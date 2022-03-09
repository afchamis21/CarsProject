import sys
import webbrowser
import cursor as cursor
import pyodbc
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication, QTableWidgetItem, QHeaderView, QDialog, \
    QFileDialog
from PyQt5.QtCore import QFileInfo
import imagens.imagens
import time
from getmac import get_mac_address as gma
import yagmail
from fpdf import FPDF


class User:
    def __init__(self, usuario, nome, sobrenome, email):
        self.usuario = usuario
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi(r"paginas/LoginScreen.ui", self)
        self.login_button.clicked.connect(self.login)
        self.password_edit.returnPressed.connect(self.login)
        self.banco_button.clicked.connect(self.open_pop_up)
        self.label_2.setText(f'Licença Válida Até: {due_date}')
        if mensagem in ['Licença de Uso Vencida', 'Licença de Uso Inválida', 'SQL Não Conectado']:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText(mensagem)

    def login(self):
        # Cria variáveis globais para uso futuro e faz o ‘login’ conferindo user e senha no SQL além de habilitar a função
        # De lembrar do usuário, transformando uma coluna do SQL, para o usuário, em 1
        if self.error_label.text() in ['Licença de Uso Vencida', 'Licença de Uso Inválida']:
            return
        username = self.login_edit.text()
        password = self.password_edit.text()
        if password != '':
            query = f"SELECT * FROM logins WHERE loginUsuario = '{username}' and pwdcompare('{password}', senhaUsuario) = 1"
            try:
                cur.execute(query)
                result_user = cur.fetchone()
                if not result_user:
                    self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                    self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                    self.error_label.setText('Usuário ou Senha Incorretos')
                elif username == result_user[1]:
                    query_update = f"UPDATE logins SET record_User='0'"
                    cur.execute(query_update)
                    connection.commit()
                    if self.RememberLoginBox.isChecked() is True:
                        query_user = f"UPDATE logins SET record_User = '1' WHERE loginUsuario='{username}'"
                        cur.execute(query_user)
                        connection.commit()
                    if username == 'admin':
                        register_window = RegisterWindow()
                        widget.addWidget(register_window)
                        widget.setCurrentIndex(widget.currentIndex() + 1)
                        widget.showMaximized()
                    else:
                        query_data = f"SELECT * FROM logins WHERE loginUsuario = '{username}'"
                        cur.execute(query_data)
                        user_variables = cur.fetchone()[3:6]
                        user_name = user_variables[0]
                        user_surname = user_variables[1]
                        user_email = user_variables[2]
                        logged_in_user = User(username, user_name, user_surname, user_email)
                        main_window = MainWindow(logged_in_user)
                        widget.addWidget(main_window)
                        widget.setCurrentIndex(widget.currentIndex() + 1)
                        widget.showMaximized()
            except:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                self.error_label.setText('Ocorreu um erro.')
        else:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Preencha a Senha')

    @staticmethod
    def open_pop_up():
        warning_popup_window = AvisoPopup()
        warning_popup_window.open_pop()


class LicenceWarningPopUp(QDialog):
    def __init__(self):
        super(LicenceWarningPopUp, self).__init__()
        loadUi(r"paginas/AvisoLicensaPopUp.ui", self)
        self.setFixedHeight(150)
        self.setFixedWidth(250)
        self.OK_button.clicked.connect(self.close)

    def open_license_pop_up(self):
        self.content_label.setText(f'Sua licença de uso expira em {due_date}')
        self.exec_()


class AvisoPopup(QDialog):
    def __init__(self):
        super(AvisoPopup, self).__init__()
        loadUi(r"paginas/AvisoPopup.ui", self)
        self.setWindowTitle('Banco de Dados')
        self.setFixedHeight(160)
        self.setFixedWidth(226)
        self.OK_button.clicked.connect(self.banco_edit_popup)

    def open_pop(self):
        self.exec_()

    def banco_edit_popup(self):
        sql_popup_window = BancoEditPopup()
        sql_popup_window.open_pop()
        self.close()


class BancoEditPopup(QDialog):
    def __init__(self):
        super(BancoEditPopup, self).__init__()
        loadUi(r"paginas/BancoEditPopup.ui", self)
        self.setWindowTitle('Banco de Dados')
        self.setFixedHeight(160)
        self.setFixedWidth(226)
        self.OK_button.clicked.connect(self.create_txt)
        with open(r"conexao/connection.txt", "r") as file:
            content = file.read()
        server = content.split(';')[0][7:]
        banco = content.split(';')[1][9:]
        self.server_edit.setText(server)
        self.banco_edit.setText(banco)

    def open_pop(self):
        self.exec_()

    def create_txt(self):
        with open(r"conexao/connection.txt", "w") as file:
            server = self.server_edit.text()
            banco = self.banco_edit.text()
            file.write(f"Server={server};Database={banco};")
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, user):
        super(MainWindow, self).__init__()
        loadUi("paginas/MainScreen.ui", self)
        self.user = user
        self.Consult_Button.clicked.connect(self.go_to_consult)
        self.Add_Button.clicked.connect(self.go_to_add)
        self.Delete_Button.clicked.connect(self.go_to_alter)
        self.Logout_Button_2.clicked.connect(self.go_to_login)
        self.user_pushButton.clicked.connect(self.go_to_config)
        self.name_label.setText(self.user.nome)
        self.label_3.setText(f'Licença Válida Até: {due_date}')

    @staticmethod
    def go_to_login():
        # Realiza logout e vai pra tela de login
        log_in_page = LoginWindow()
        widget.addWidget(log_in_page)
        try:
            query_remember_user = "SELECT loginUsuario FROM logins WHERE record_User = 1"
            cur.execute(query_remember_user)
            remembered_user_from_main = cur.fetchone()[0]
            log_in_page.login_edit.setText(remembered_user_from_main)
            log_in_page.RememberLoginBox.setChecked(True)
        except:
            log_in_page.login_edit.setText('')
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_config(self):
        # Vai para a página de configuração
        config_page = ConfigWindow(self.user)
        widget.addWidget(config_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_consult(self):
        # Vai para a página de consulta
        consult_page = ConsultWindow(self.user)
        widget.addWidget(consult_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_add(self):
        # Vai para a página de adicionar ao SQL
        add_page = AddWindow(self.user)
        widget.addWidget(add_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_alter(self):
        # Vai para a página de editar dados do SQL
        alteration_page = AlterationVehicleWindow(self.user)
        widget.addWidget(alteration_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ConsultWindow(QMainWindow):
    def __init__(self, user):
        super(ConsultWindow, self).__init__()
        loadUi(r"paginas/ConsultScreen.ui", self)
        self.user = user
        self.consult_button.clicked.connect(self.search_data_base)
        self.tableWidget.itemClicked.connect(self.select_date)
        self.back_button.clicked.connect(self.go_back)
        self.mail_button.clicked.connect(self.open_pop_up)
        self.download_button.clicked.connect(self.create_pdf)
        self.consult_edit.returnPressed.connect(self.search_data_base)
        self.edit_button.clicked.connect(self.go_to_alter)
        self.right_button.clicked.connect(self.increase_index)
        self.left_button.clicked.connect(self.decrease_index)
        self.listWidget.itemDoubleClicked.connect(self.open_docs)
        self.consult_edit.textEdited.connect(self.edit_date)
        self.filter_comboBox.currentIndexChanged.connect(self.check_for_date)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cursor_positions = [0]
        self.reports = []
        self.listWidget.hide()
        self._images = []
        self._index_images = 0
        self._documents = []

    def check_for_date(self):
        selector = self.filter_comboBox.currentText()
        if selector == 'Data de Entrada' or selector == 'Data de Saida':
            self.consult_edit.setText('')

    def edit_date(self):
        selector = self.filter_comboBox.currentText()
        if selector == 'Data de Entrada' or selector == 'Data de Saida':
            text = self.consult_edit.text()
            position = self.consult_edit.cursorPosition()
            if position > self.cursor_positions[-1]:
                if len(text) == 2 or len(text) == 5:
                    self.consult_edit.setText(f'{text}/')
            self.cursor_positions.append(position)

    def go_to_alter(self):
        alteration_page = AlterationVehicleWindow(self.user)
        widget.addWidget(alteration_page)
        try:
            plate = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            alteration_page.placaAtual_edit.setText(plate)
        except:
            pass
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def open_pop_up(self):
        # Cria o arquivo excel e abre o popup
        self.create_pdf()
        popup_window = EmailPopUpWindow(self, self.user)
        popup_window.open_page()

    def create_pdf(self):
        with open("conexao/config_relatorio.txt", "r") as relatorio_config:
            content = int(relatorio_config.read())
        self.reports = []
        if content:
            self.create_multiple_pdf()
        else:
            self.create_unique_pdf()

    def create_multiple_pdf(self):
        t = time.localtime()
        current_date = time.strftime("%d-%m", t)

        rows = self.tableWidget.rowCount()
        if not rows:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Tabela Vazia')
            return
        columns = self.tableWidget.columnCount()

        try:
            for row in range(rows):
                filename = f'relatorios/Relatório PLACA {self.tableWidget.item(row, 0).text()} {current_date}.pdf'
                self.reports.append(filename)
                pdf = FPDF('P', 'mm', 'A4')
                pdf.add_page()
                pdf.set_auto_page_break(True, 10)
                pdf.set_font("helvetica", size=12)

                pdf.cell(0, txt=filename.split('/')[1][:-4], ln=1, align='C')
                pdf.set_font("helvetica", size=8)

                height_top = 50
                height_bottom = -45
                for column in range(columns):
                    data = self.tableWidget.item(row, column).text()
                    if not data:
                        data = 'N/A'

                    if column == 0:
                        pdf.cell(-1, height_top, txt="Placa", align='L')
                        pdf.cell(52, height_top + 10, txt=data, align='L')

                    elif column == 1:
                        pdf.cell(-1, height_top, txt="Modelo", align='L')
                        pdf.cell(52, height_top + 10, txt=data, align='L')

                    elif column == 2:
                        pdf.cell(-1, height_top, txt="RDO", align='L')
                        pdf.cell(52, height_top + 10, txt=data, align='L')

                    elif column == 3:
                        pdf.cell(-1, height_top, txt="DP", align='L')
                        pdf.cell(52, height_top + 10, txt=data, ln=1, align='L')

                    elif column == 4:
                        pdf.cell(-1, height_bottom, txt="Status", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, align='L')

                    elif column == 5:
                        pdf.cell(-1, height_bottom, txt="Patio do Veículo", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, align='L')

                    elif column == 6:
                        pdf.cell(-1, height_bottom, txt="Data Entrada", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, align='L')

                    elif column == 7:
                        pdf.cell(-1, height_bottom, txt="Data Saída", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, ln=1, align='L')

                pdf.cell(0, 10, ln=1)
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet("color: rgb(102,142,57);")
                self.error_label.setText('Relatório Criado')
                pdf.output(filename)

        except:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Impossível Criar os Relatórios')
            return

    def create_unique_pdf(self):
        t = time.localtime()
        current_date = time.strftime("%d-%m", t)
        selector = self.filter_comboBox.currentText()
        search = self.consult_edit.text().upper()
        filename = f'relatorios/Relatório {selector} {search} {current_date}.pdf'
        self.reports.append(filename)
        rows = self.tableWidget.rowCount()
        if not rows:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Tabela Vazia')
            return
        columns = self.tableWidget.columnCount()

        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_auto_page_break(True, 10)
        pdf.set_font("helvetica", size=12)

        pdf.cell(0, txt=filename.split('/')[1][:-4], ln=1, align='C')
        pdf.set_font("helvetica", size=8)

        height_top = 50
        height_bottom = -45
        try:
            for row in range(rows):
                for column in range(columns):
                    data = self.tableWidget.item(row, column).text()
                    if not data:
                        data = 'N/A'

                    if column == 0:
                        pdf.cell(-1, height_top, txt="Placa", align='L')
                        pdf.cell(52, height_top + 10, txt=data, align='L')

                    elif column == 1:
                        pdf.cell(-1, height_top, txt="Modelo", align='L')
                        pdf.cell(52, height_top + 10, txt=data, align='L')

                    elif column == 2:
                        pdf.cell(-1, height_top, txt="RDO", align='L')
                        pdf.cell(52, height_top + 10, txt=data, align='L')

                    elif column == 3:
                        pdf.cell(-1, height_top, txt="DP", align='L')
                        pdf.cell(52, height_top + 10, txt=data, ln=1, align='L')

                    elif column == 4:
                        pdf.cell(-1, height_bottom, txt="Status", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, align='L')

                    elif column == 5:
                        pdf.cell(-1, height_bottom, txt="Patio do Veículo", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, align='L')

                    elif column == 6:
                        pdf.cell(-1, height_bottom, txt="Data Entrada", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, align='L')

                    elif column == 7:
                        pdf.cell(-1, height_bottom, txt="Data Saída", align='L')
                        pdf.cell(52, height_bottom + 10, txt=data, ln=1, align='L')

                pdf.cell(0, 10, ln=1)
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet("color: rgb(102,142,57);")
            self.error_label.setText('Relatório Criado')
            pdf.output(filename)
        except:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Impossível Criar Relatório')
            return

    def go_back(self):
        # Retorna para a página principal
        main_page = MainWindow(self.user)
        widget.addWidget(main_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def increase_index(self):
        if self._images:
            self._index_images += 1
            if self._index_images >= len(self._images):
                self._index_images = 0
            self.show_image()

    def decrease_index(self):
        if self._images:
            self._index_images -= 1
            if self._index_images < len(self._images) * -1:
                self._index_images = len(self._images) - 1
            self.show_image()

    def show_image(self):
        self.image_label.setStyleSheet(
            f"background-color: rgb(0, 0, 0); border-image: url({self._images[self._index_images]}); background-position: center; background-repeat: norepeat;")

    def open_docs(self):
        doc = self.listWidget.currentItem().text()
        webbrowser.open(doc)

    def _reset_image(self):
        self.image_label.setStyleSheet(
            "background-color: rgb(0, 0, 0); border-image: url(); background-position: center; background-repeat: norepeat;")

    def select_all_images(self):
        images = []
        for line in range(self.tableWidget.rowCount()):
            plate = self.tableWidget.item(line, 0).text()
            query_time = f"SELECT * FROM registros WHERE placa = '{plate}'"
            cur.execute(query_time)
            result_time = cur.fetchall()[0]
            image_name = result_time[10]
            if image_name:
                images.append(image_name)
        return images

    def select_all_documents(self):
        documents = []
        for line in range(self.tableWidget.rowCount()):
            plate = self.tableWidget.item(line, 0).text()
            query_time = f"SELECT * FROM registros WHERE placa = '{plate}'"
            cur.execute(query_time)
            result_time = cur.fetchall()[0]
            doc_name = result_time[11]
            if doc_name:
                documents.append(doc_name)
        return documents

    def select_date(self):
        # Mostra a data, horário e imagem, se cadastrada, de registro, específicos de um veículo ao clicar na linha
        plate = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        query_time = f"SELECT * FROM registros WHERE placa = '{plate}'"
        cur.execute(query_time)
        result_time = cur.fetchall()[0]
        data = result_time[8]
        hora = result_time[9]
        image_name = result_time[10]
        documents = result_time[11]
        if documents:
            self._documents = documents.split(';')
            self._show_docs()
        else:
            self.listWidget.clear()
        if image_name:
            self._images = image_name.split(';')
            self._index_images = 0
            self.image_label.setStyleSheet(
                f"background-color: rgb(0, 0, 0); border-image: url({self._images[self._index_images]}); background-position: center; background-repeat: norepeat;")
        else:
            self._reset_image()
        formatted_date = format_date_from_sql(data)
        self.hora_label.setText(hora[:-8])
        self.data_label.setText(formatted_date)

    def _show_docs(self):
        if self.listWidget.count() != 0:
            self.listWidget.clear()
        for doc in self._documents:
            self.listWidget.addItem(doc)

    def search_data_base(self):
        # Realiza as consultas no SQL e mostra na tabela
        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 0); border-radius: 10px;")
        self.error_label.setText('')
        selector = self.filter_comboBox.currentText()
        search = self.consult_edit.text().upper()

        if selector == 'Placa':
            query_search = f"SELECT * FROM registros WHERE placa LIKE '%{search}%'"
            cur.execute(query_search)
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0

        elif selector == 'Modelo':
            query_search = f"SELECT * FROM registros WHERE veiculo LIKE '%{search}%'"
            cur.execute(query_search)
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0

        elif selector == 'RDO':
            query_search = f"SELECT * FROM registros WHERE RDO LIKE '%{search}%'"
            cur.execute(query_search)
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0

        elif selector == 'DP':
            query_search = f"SELECT * FROM registros WHERE DP LIKE '%{search}%'"
            cur.execute(query_search)
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0

        elif selector == 'Status':
            query_search = f"SELECT * FROM registros WHERE estatus LIKE '%{search}%'"
            cur.execute(query_search)
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0

        elif selector == 'Patio L.':
            query_search = f"SELECT * FROM registros WHERE patio LIKE '%{search}%'"
            cur.execute(query_search)
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0

        elif selector == 'Data de Entrada':
            try:
                query_search = f"SELECT * FROM registros WHERE dataE = '{search}'"
                cur.execute(query_search)
            except:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                self.error_label.setText('Data Inválida')
                return
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0

        elif selector == 'Data de Saida':
            try:
                query_search = f"SELECT * FROM registros WHERE dataS = '{search}'"
                cur.execute(query_search)
            except:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                self.error_label.setText('Data Inválida')
                return
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            column = 0
            row = 0
            for car in result:
                for data in car[:-4]:
                    if column == 6:
                        data = format_date_from_sql(data)
                    elif column == 7:
                        if data:
                            data = format_date_from_sql(data)
                    self.tableWidget.setItem(row, column, QTableWidgetItem(data))
                    self.tableWidget.item(row, column).setToolTip(f"<font color=white>{data}</font>")
                    column += 1
                row += 1
                column = 0


class EmailPopUpWindow(QDialog):
    def __init__(self, parent, user):
        super(EmailPopUpWindow, self).__init__()
        loadUi("paginas/ImageNamePopup.ui", self)
        self.user = user
        self.setWindowTitle('Envio de E-mail')
        self.save_button.clicked.connect(self.send_mail)
        self.textEdit.textChanged.connect(self.switch_color_message)
        self.assunto_edit.textChanged.connect(self.switch_color_subject)
        self.file_button.clicked.connect(self.select_files)
        self.imagens_checkBox.stateChanged.connect(self.attach_images)
        self.documentos_checkBox.stateChanged.connect(self.attach_docs)
        self.relatorios_checkBox.stateChanged.connect(self.attach_report)
        self.remover_button.clicked.connect(self.delete_file)
        self.listWidget.hide()
        self._subject_config = ''
        self._message_config = ''
        self._contents_message = ''
        self._auto_message = ''
        self.parent = parent
        self._files = []
        self._total_size = 0
        self.check_configurations()
        self.check_message()

    def open_page(self):
        self.exec_()

    def check_configurations(self):
        with open("conexao/email_configurations.txt", "r") as email_config:
            content = email_config.read()
            if content:
                if '/' in content:
                    self._subject_config = content.split('/')[0].strip()
                    self._message_config = content.split('/')[1].strip()
        if self._subject_config:
            if len(self.parent.reports) == 1:
                self.assunto_edit.setText(self.parent.reports[0].split('/')[1][:-4])
            else:
                assunto = 'Relatório'
                for file in self.parent.reports:
                    name = file.split('/')[1][:-4] + ', '
                    assunto += name.replace('Relatório', '')
                self.assunto_edit.setText(assunto[:-2])
        if self._message_config:
            if """#saudacao,

Segue em anexo #conteudo, referentes ao #nome_do_arquivo

Att""" == self._message_config:
                self._auto_message = self._message_config
            self.textEdit.setPlainText(self._message_config)

    def check_message(self):
        t = time.localtime()
        current_hour = int(time.strftime("%H", t))
        if 6 <= current_hour <= 12:
            greetings = 'Bom dia'
        elif 12 < current_hour <= 18:
            greetings = 'Boa tarde'
        else:
            greetings = 'Boa noite'
        if self.parent.reports:
            assunto = 'Relatório'
            for file in self.parent.reports:
                name = file.split('/')[1][:-4] + ', '
                assunto += name.replace('Relatório', '')
            self._message_config = self._message_config.replace("#saudacao", greetings).replace("#nome_do_arquivo",
                                                                                                assunto[:-2])
        self.textEdit.setPlainText(self._message_config)

    @staticmethod
    def convert_size(size):
        if size >= 1048576:
            result_size = f"{size * 0.00000095367432 :.2f} MB"
        elif size >= 1024:
            result_size = f"{size * 0.0009765625 :.2f} KB"
        else:
            result_size = f"{size} Bytes"
        return result_size

    def _update_size(self):
        if self._total_size >= 1048576:
            size = f"{self._total_size * 0.00000095367432 :.2f} MB"
        elif self._total_size >= 1024:
            size = f"{self._total_size * 0.0009765625:.2f} KB"
        else:
            size = f"{self._total_size} Bytes"
        if self._total_size > 26214400:
            self.mb_label.setStyleSheet("color: rgb(255, 0, 0);")
            self.mb_label.setText(f"Tamanho Excedido {size}")
        else:
            self.mb_label.setStyleSheet("color: rgb(188, 188, 188);")
            self.mb_label.setText(size)

    def _update_list(self):
        self.listWidget.clear()
        for kind, file in self._files:
            info = QFileInfo(file)
            size = info.size()
            self.listWidget.addItem(f"{self.convert_size(size)} - {file}")

    def delete_file(self):
        if self.listWidget.currentItem():
            item = self.listWidget.currentRow()

            file = self.listWidget.takeItem(item)
            file_text = file.text()
            file_list = file_text.split('-')
            if len(file_list) > 2:
                file_name = '-'.join(file_list[1:]).strip()
            else:
                file_name = file_list[1].strip()

            self.remove_file(file_name)

    def remove_file(self, file_name):
        substitute = []
        verifier = 0
        for content in self._files:
            file = content[1]
            if file != file_name or verifier == 1:
                substitute.append(content)
            else:
                verifier = 1
                info = QFileInfo(file)
                size = info.size()
                self._total_size -= size
        self._files = substitute

        self._update_list()
        self._update_size()

    def select_files(self):
        arquivo = QFileDialog.getOpenFileName(self, 'Selecione o Arquivo', '', 'Todos Arquivos (*.*)')
        support_list = [item[1] for item in self._files]
        if arquivo:
            doc_path = arquivo[0]
            if doc_path:
                info = QFileInfo(doc_path)
                size = info.size()
                if doc_path not in support_list:
                    self._files.append(('file', doc_path))
                    self._total_size += size

                    self._update_size()
                    self._update_list()

    def attach_images(self):
        if self.imagens_checkBox.isChecked():
            images = self.parent.select_all_images()
            for image in images:
                image_list = image.split(';')
                for image_final in image_list:
                    self._files.append(('img', image_final))
                    info = QFileInfo(image_final)
                    size = info.size()
                    self._total_size += size
            self._contents_message += 'as imagens; '
        else:
            substitute = []
            for content in self._files:
                kind = content[0]
                file = content[1]
                if kind != 'img':
                    substitute.append(content)
                else:
                    info = QFileInfo(file)
                    size = info.size()
                    self._total_size -= size
            self._files = substitute
            self._contents_message = self._contents_message.replace('as imagens; ', '')
            self._contents_message = self._contents_message.replace('as imagens', '')

        self._update_size()
        self._update_list()
        self._update_contents()

    def attach_docs(self):
        if self.documentos_checkBox.isChecked():
            docs = self.parent.select_all_documents()
            if docs:
                for document in docs:
                    document_list = document.split(';')
                    for document_final in document_list:
                        self._files.append(('doc', document_final))
                        info = QFileInfo(document_final)
                        size = info.size()
                        self._total_size += size
            self._contents_message += 'os documentos; '
        else:
            substitute = []
            for content in self._files:
                kind = content[0]
                file = content[1]
                if kind != 'doc':
                    substitute.append(content)
                else:
                    info = QFileInfo(file)
                    size = info.size()
                    self._total_size -= size
            self._files = substitute
            self._contents_message = self._contents_message.replace('os documentos; ', '')
            self._contents_message = self._contents_message.replace('os documentos', '')

        self._update_size()
        self._update_list()
        self._update_contents()

    def attach_report(self):
        if self.relatorios_checkBox.isChecked():
            for file in self.parent.reports:
                self._files.append(('report', file))
                info = QFileInfo(file)
                size = info.size()
                self._total_size += size
            self._contents_message += 'o relatório; '
        else:
            substitute = []
            for content in self._files:
                kind = content[0]
                file = content[1]
                if kind != 'report':
                    substitute.append(content)
                else:
                    info = QFileInfo(file)
                    size = info.size()
                    self._total_size -= size
            self._files = substitute
            self._contents_message = self._contents_message.replace('o relatório; ', '')
            self._contents_message = self._contents_message.replace('o relatório', '')

        self._update_size()
        self._update_list()
        self._update_contents()

    def _update_contents(self):
        if self._auto_message:
            content = self._message_config.split('#')[1].split(',')[0]
            self._contents_message = self._contents_message.replace('/', '')
            if not self._contents_message:
                self._contents_message = '/'
                self._message_config = self._message_config.replace(content, self._contents_message)
            else:
                self._message_config = self._message_config.replace(content, self._contents_message[:-2])

            self.textEdit.setPlainText(self._message_config)

    @staticmethod
    def decrypt(message):
        # decript function
        return result_message

    def send_mail(self):
        # Envia o e-mail de relatório da tabela para o e-mail atrelado ao usuário.
        try:
            if self._total_size > 26214400:
                return
            if not self.email_edit.text() or '@' not in self.email_edit.text():
                self.email_edit.setPlaceholderText('Email (Campo Obrigatório)')
                return

            get_login_query = f"SELECT email_login, email_senha FROM logins WHERE loginUsuario = '{self.user.usuario}'"
            cur.execute(get_login_query)
            login_info = cur.fetchone()
            email = login_info[0]
            senha = self.decrypt(login_info[1])

            usuario = yagmail.SMTP(user=email, password=senha)
            remetentes = [emails.strip() for emails in self.email_edit.text().split(';')]
            if self.assunto_edit.text():
                assunto = self.assunto_edit.text()
            else:
                assunto = ''

            if self.textEdit.toPlainText():
                content = self.textEdit.toPlainText().replace('#/', '').replace('#', '')
            else:
                content = ""

            files = [file[1] for file in self._files if QFileInfo(file[1]).size() != 0]
            usuario.send(to=remetentes, subject=assunto, contents=content, attachments=files)
            self.parent.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.parent.error_label.setStyleSheet("color: rgb(102,142,57);")
            self.parent.error_label.setText('Email Enviado')
            self.close()
        except:
            self.parent.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.parent.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.parent.error_label.setText('Email Não Enviado')
            self.close()

    def switch_color_message(self):
        if len(self.textEdit.toPlainText()) == 1:
            self.textEdit.setStyleSheet(
                "QTextEdit{border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: 5px; background-color: rgb(255,255,255);    color: rgb(0,0,0);}"
                "QTextEdit:hover{ border: 2px solid rgb(117, 117, 179);}"
                "QTextEdit:focus{ border: 2px solid rgb(117, 117, 179); color: rgb(40, 40, 40);}")
        if not self.textEdit.toPlainText():
            self.textEdit.setStyleSheet(
                "QTextEdit{border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: 5px; background-color: rgb(238,238,238);    color: rgb(0,0,0);}"
                "QTextEdit:hover{ border: 2px solid rgb(117, 117, 179);}"
                "QTextEdit:focus{ border: 2px solid rgb(117, 117, 179); color: rgb(40, 40, 40);}")

    def switch_color_subject(self):
        if len(self.assunto_edit.text()) == 1:
            self.assunto_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: 5px; background-color: rgb(255,255,255);    color: rgb(0,0,0);}"
                "QLineEdit:hover{ border: 2px solid rgb(117, 117, 179);}"
                "QLineEdit:focus{ border: 2px solid rgb(117, 117, 179); color: rgb(40, 40, 40);}")
        if not self.assunto_edit.text():
            self.assunto_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: 5px; background-color: rgb(238,238,238);    color: rgb(0,0,0);}"
                "QLineEdit:hover{ border: 2px solid rgb(117, 117, 179);}"
                "QLineEdit:focus{ border: 2px solid rgb(117, 117, 179); color: rgb(40, 40, 40);}")


class FilesPopUp(QDialog):
    def __init__(self, parent):
        super(FilesPopUp, self).__init__()
        loadUi("paginas/DocPopup.ui", self)
        self.setWindowTitle('Selecionar Arquivos')
        self.adicionar_button.clicked.connect(self.add_items)
        self.excluir_button.clicked.connect(self.delete_item)
        self.visualizar_button.clicked.connect(self.visualize_item)
        self.save_button.clicked.connect(self.send_result)
        self._parent = parent
        self._files = []

    def show_from_parent(self):
        for file in self._parent.documents:
            self.listWidget.addItem(file)
            self._files.append(file)

    def open_popup(self):
        self.exec_()

    def add_items(self):
        arquivo = QFileDialog.getOpenFileName(self, 'Selecione o Arquivo', '', 'Todos Arquivos (*.*)')
        if arquivo:
            doc_path = arquivo[0]
            if doc_path:
                self.listWidget.addItem(doc_path)
                self._files.append(doc_path)

    def delete_item(self):
        if self.listWidget.currentItem():
            item = self.listWidget.currentRow()
            item_object = self.listWidget.takeItem(item)
            item_text = item_object.text()
            self._files.remove(item_text)

    def visualize_item(self):
        if self.listWidget.currentItem():
            item = self.listWidget.currentItem()
            webbrowser.open(item.text())

    def send_result(self):
        self._parent.documents = self._files
        self.close()


class AddWindow(QMainWindow):
    def __init__(self, user):
        super(AddWindow, self).__init__()
        loadUi("paginas/RegisterVehicleScreen.ui", self)
        self.user = user
        self.status_comboBox.currentIndexChanged.connect(self.set_exit_date_visible)
        self.dataS_edit.setStyleSheet(
            "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
            "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
        self.dataS_edit.setPlaceholderText('')
        self.dataS_edit.setReadOnly(True)
        self.save_button.clicked.connect(self.add_data)
        self.back_button.clicked.connect(self.go_back)
        self.image_button.clicked.connect(self.get_image)
        self.dataE_edit.textEdited.connect(self.edit_date_e)
        self.dataS_edit.textEdited.connect(self.edit_date_s)
        self.right_button.clicked.connect(self.increase_index)
        self.left_button.clicked.connect(self.decrease_index)
        self.doc_button.clicked.connect(self.get_docs)
        self.remover_button.clicked.connect(self.remove_image)
        self._images = []
        self._index = -1
        self.documents = []

    def remove_image(self):
        if self._images:
            self._images.remove(self._images[self._index])
            self.decrease_index()
            self.show_image()

    def increase_index(self):
        if self._images:
            self._index += 1
            if self._index >= len(self._images):
                self._index = 0
            self.show_image()

    def decrease_index(self):
        if self._images:
            self._index -= 1
            if self._index < len(self._images) * -1:
                self._index = len(self._images) - 1
            self.show_image()

    def get_docs(self):
        pop_up = FilesPopUp(self)
        pop_up.open_popup()

    def get_image(self):
        arquivo = QFileDialog.getOpenFileName(self, 'Selecione o Arquivo', '', 'Todos Arquivos (*.*)')
        if arquivo:
            image_path = arquivo[0]
            if image_path:
                self._images.append(image_path)
                self.increase_index()

    def show_image(self):
        if self._images:
            image_path = self._images[self._index]
            self.imagem_label.setStyleSheet(
                f"background-color: rgb(0, 0, 0); border-image: url({image_path}); background-position: center; background-repeat: norepeat; color: rgba(0, 0, 0, 0)")
        else:
            self._reset_image()

    def edit_date_e(self):
        text = self.dataE_edit.text()
        position = self.dataE_edit.cursorPosition()
        if position > position_E_Add[-1]:
            if len(text) == 2 or len(text) == 5:
                self.dataE_edit.setText(f'{text}/')
        position_E_Add.append(position)

    def edit_date_s(self):
        text = self.dataS_edit.text()
        position = self.dataS_edit.cursorPosition()
        if position > position_S_Add[-1]:
            if len(text) == 2 or len(text) == 5:
                self.dataS_edit.setText(f'{text}/')
        position_S_Add.append(position)

    def go_back(self):
        # Retorna para a página principal
        main_page = MainWindow(self.user)
        widget.addWidget(main_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def _reset_image(self):
        self.imagem_label.setStyleSheet(
            f"background-color: rgb(0, 0, 0); border-image: url(); background-position: center; background-repeat: norepeat; color: rgba(0, 0, 0, 0)")

    def add_data(self):
        # Adiciona os dados ao SQL, com data e hora de registro
        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 0); border-radius: 10px;")
        self.error_label.setText('')
        plate = self.placa_edit.text().upper()
        rdo = self.RDO_edit.text().upper()
        entry_date = self.dataE_edit.text().upper()
        data_s = self.dataS_edit.text().upper()
        vehicle = self.vehicle_edit.text().upper()
        dp = self.DP_edit.text().upper()
        status = self.status_comboBox.currentText().upper()
        patio = self.p_edit_2.text().upper()
        images = ';'.join(self._images)
        documents = ';'.join(self.documents)

        try:
            verified_entry_date = verify_date(entry_date)
        except:
            verified_entry_date = False

        try:
            verified_exit_date = verify_date(data_s)
        except:
            verified_exit_date = False

        t = time.localtime()
        current_date = time.strftime("%d/%m/%Y", t)
        current_hour = time.strftime("%H:%M", t)
        if len(plate) == 7:
            if len(entry_date) != 0:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 0); border-radius: 10px;")
                self.error_label.setText('')
                if verified_entry_date:
                    if status == 'PATIO':
                        try:
                            query_add = f"INSERT INTO registros (placa, veiculo, RDO, DP, estatus, patio, dataE, dataR, horaR, imagens, documentos) VALUES ('{plate}', '{vehicle}', '{rdo}', '{dp}', '{status}', '{patio}', '{entry_date}', '{current_date}', '{current_hour}' , '{images}', '{documents}')"
                            cur.execute(query_add)
                            connection.commit()
                            self.placa_edit.setText('')
                            self.RDO_edit.setText('')
                            self.dataE_edit.setText('')
                            self.vehicle_edit.setText('')
                            self.DP_edit.setText('')
                            self.dataS_edit.setText('')
                            self.p_edit_2.setText('')
                            self.erro_login.setStyleSheet(
                                "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                            self.error_label.setStyleSheet('color: rgb(102,142,57);')
                            self.error_label.setText('Cadastro Bem-Sucedido')
                            self._images = []
                            self._index = 0
                            self._reset_image()
                        except:
                            self.erro_login.setStyleSheet(
                                "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                            self.error_label.setText('Placa Já Cadastrada')

                    elif status == 'RETIRADO' and len(data_s) != 0:

                        if verified_exit_date:
                            try:
                                query_add = f"INSERT INTO registros (placa, veiculo, RDO, DP, estatus, patio, dataE, dataS, dataR, horaR, imagens, documentos) VALUES ('{plate}', '{vehicle}', '{rdo}', '{dp}', '{status}', '{patio}', '{entry_date}', '{data_s}', '{current_date}', '{current_hour}', '{images}', '{documents}')"
                                cur.execute(query_add)
                                connection.commit()
                                self.placa_edit.setText('')
                                self.RDO_edit.setText('')
                                self.dataE_edit.setText('')
                                self.vehicle_edit.setText('')
                                self.DP_edit.setText('')
                                self.p_edit_2.setText('')
                                self.dataS_edit.setText('')
                                self.erro_login.setStyleSheet(
                                    "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                                self.error_label.setStyleSheet('color: rgb(102,142,57);')
                                self.error_label.setText('Cadastro Bem-Sucedido')
                                self._images = []
                                self._index = 0
                                self._reset_image()

                            except:
                                self.erro_login.setStyleSheet(
                                    "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                                self.error_label.setText('Placa Já Cadastrada')
                                return
                        else:
                            self.erro_login.setStyleSheet(
                                "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                            self.error_label.setText('Data de Saída Inválida')
                    elif status == 'RETIRADO' and len(data_s) == 0:
                        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                        self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                        self.error_label.setText('Preencha a Data de Saída')
                else:
                    self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                    self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                    self.error_label.setText('Data de Entrada Inválida')
            else:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                self.error_label.setText('Preencha uma Data de Entrada')
        else:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Placa Inválida')

    def set_exit_date_visible(self):
        # Altera a visibilidade da caixa de data de saída com base no seletor de status
        if self.status_comboBox.currentIndex() == 0:
            self.dataS_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
                "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
            self.dataS_edit.setPlaceholderText('')
            self.dataS_edit.setText('')
            self.dataS_edit.setReadOnly(True)
        elif self.status_comboBox.currentIndex() == 1:
            self.dataS_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: "
                "5px; background-color: rgb(255,255,255); color: rgb(0,0,0);} QLineEdit:hover{"
                "border: 2px solid rgb(117, 117, 179);} QLineEdit:focus{border: 2px solid rgb("
                "117, 117, 179); color: rgb(40, 40, 40);}")
            self.dataS_edit.setPlaceholderText("Data de Saida (DD/MM/AAAA)")
            self.dataS_edit.setReadOnly(False)


class AlterationVehicleWindow(QMainWindow):
    def __init__(self, user):
        super(AlterationVehicleWindow, self).__init__()
        loadUi("paginas/AlterationVehicleScreen.ui", self)
        self.user = user
        self.dataS_edit.setStyleSheet(
            "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
            "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
        self.dataS_edit.setPlaceholderText('')
        self.dataS_edit.setReadOnly(True)
        self.status_comboBox.currentIndexChanged.connect(self.set_exit_date_visible)
        self.save_button.clicked.connect(self.add_data)
        self.back_button.clicked.connect(self.go_back)
        self.placaAtual_edit.editingFinished.connect(self.info)
        self.image_button.clicked.connect(self.get_image)
        self.dataE_edit.textEdited.connect(self.edit_date_e)
        self.dataS_edit.textEdited.connect(self.edit_date_s)
        self.right_button.clicked.connect(self.increase_index)
        self.left_button.clicked.connect(self.decrease_index)
        self.remover_button.clicked.connect(self.remove_image)
        self.doc_button.clicked.connect(self.get_docs)
        self._images = []
        self._index = 0
        self.documents = []

    def remove_image(self):
        if self._images:
            self._images.remove(self._images[self._index])
            self.decrease_index()
            self.show_image()

    def increase_index(self):
        if self._images:
            self._index += 1
            if self._index >= len(self._images):
                self._index = 0
            self.show_image()

    def decrease_index(self):
        if self._images:
            self._index -= 1
            if self._index < len(self._images) * -1:
                self._index = len(self._images) - 1
            self.show_image()

    def get_docs(self):
        pop_up = FilesPopUp(self)
        pop_up.show_from_parent()
        pop_up.open_popup()

    def get_image(self):
        arquivo = QFileDialog.getOpenFileName(self, 'Selecione o Arquivo', '', 'Todos Arquivos (*.*)')
        if arquivo:
            image_path = arquivo[0]
            if image_path:
                self._images.append(image_path)
                self.increase_index()

    def show_image(self):
        if self._images:
            image_path = self._images[self._index]
            self.imagem_label.setStyleSheet(
                f"background-color: rgb(0, 0, 0); border-image: url({image_path}); background-position: center; background-repeat: norepeat; color: rgba(0, 0, 0, 0)")
        else:
            self._reset_image()

    def edit_date_e(self):
        text = self.dataE_edit.text()
        position = self.dataE_edit.cursorPosition()
        if position > position_E_Alter[-1]:
            if len(text) == 2 or len(text) == 5:
                self.dataE_edit.setText(f'{text}/')
        position_E_Alter.append(position)

    def edit_date_s(self):
        text = self.dataS_edit.text()
        position = self.dataS_edit.cursorPosition()
        if position > position_S_Alter[-1]:
            if len(text) == 2 or len(text) == 5:
                self.dataS_edit.setText(f'{text}/')
        position_S_Alter.append(position)

    def info(self):
        plate = self.placaAtual_edit.text()
        query_info = f"select * from registros where placa = '{plate}'"
        cur.execute(query_info)
        result_info = cur.fetchone()[0:12]
        placa = result_info[0]
        veiculo = result_info[1]
        rdo = result_info[2]
        dp = result_info[3]
        status = result_info[4].upper()
        patio = result_info[5]
        data_e = result_info[6]
        data_e = format_date_from_sql(data_e)
        data_s = result_info[7]
        self._images = result_info[10].split(';') if result_info[10] else []
        self.documents = result_info[11].split(';') if result_info[11] else []
        if status == 'PATIO':
            self.status_comboBox.setCurrentIndex(0)
        elif status == 'RETIRADO':
            self.status_comboBox.setCurrentIndex(1)
            data_s = format_date_from_sql(data_s)
        self.placa_edit.setText(placa)
        self.vehicle_edit.setText(veiculo)
        self.RDO_edit.setText(rdo)
        self.DP_edit.setText(dp)
        self.p_edit_2.setText(patio)
        self.dataE_edit.setText(data_e)
        self.dataS_edit.setText(data_s)
        self.show_image()

    def go_back(self):
        main_page = MainWindow(self.user)
        widget.addWidget(main_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def _reset_image(self):
        self.imagem_label.setStyleSheet(
            f"background-color: rgb(0, 0, 0); border-image: url(); background-position: center; background-repeat: norepeat; color: rgba(0, 0, 0, 0)")

    def add_data(self):
        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 0); border-radius: 10px;")
        self.error_label.setText('')
        plate = self.placaAtual_edit.text().upper()
        placa = self.placa_edit.text().upper()
        rdo = self.RDO_edit.text().upper()
        data_e = self.dataE_edit.text().upper()
        veiculo = self.vehicle_edit.text().upper()
        dp = self.DP_edit.text().upper()
        patio = self.p_edit_2.text().upper()
        data_s = self.dataS_edit.text().upper()
        status = self.status_comboBox.currentText().upper()
        images = ';'.join(self._images)
        documentos = ';'.join(self.documents)
        t = time.localtime()
        current_date = time.strftime("%d/%m/%Y", t)
        current_hour = time.strftime("%H:%M", t)
        try:
            verified_entry_date = verify_date(data_e)
        except:
            verified_entry_date = False

        try:
            verified_exit_date = verify_date(data_s)
        except:
            verified_exit_date = False

        if len(placa) == 7:
            if verified_entry_date:
                if status == 'PATIO':
                    try:
                        query_add = f"UPDATE  registros SET placa='{placa}', veiculo='{veiculo}', RDO='{rdo}', DP='{dp}', estatus='{status}', patio = '{patio}', dataE='{data_e}', dataS=NULL, dataR='{current_date}', horaR='{current_hour}', imagens='{images}', documentos='{documentos}' WHERE placa='{plate}'"
                        cur.execute(query_add)
                        connection.commit()
                        self.placaAtual_edit.setText('')
                        self.placa_edit.setText('')
                        self.RDO_edit.setText('')
                        self.dataE_edit.setText('')
                        self.vehicle_edit.setText('')
                        self.DP_edit.setText('')
                        self.dataS_edit.setText('')
                        self.p_edit_2.setText('')
                        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                        self.error_label.setStyleSheet('color: rgb(102,142,57);')
                        self.error_label.setText('Alteração Bem-Sucedida')
                        self._images = []
                        self._index = 0
                        self._reset_image()
                    except:
                        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                        self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                        self.error_label.setText('Placa Já Cadastrada')
                        return

                elif status == 'RETIRADO' and len(data_s) != 0:
                    if verified_exit_date:
                        try:
                            query_add = f"UPDATE  registros SET placa = '{placa}', veiculo='{veiculo}', RDO='{rdo}', DP='{dp}', estatus='{status}', patio = '{patio}', dataE='{data_e}', dataS='{data_s}', dataR='{current_date}', horaR='{current_hour}', imagens='{images}' ,documentos='{documentos}' WHERE placa='{plate}'"
                            cur.execute(query_add)
                            connection.commit()
                            self.placaAtual_edit.setText('')
                            self.placa_edit.setText('')
                            self.RDO_edit.setText('')
                            self.dataE_edit.setText('')
                            self.vehicle_edit.setText('')
                            self.DP_edit.setText('')
                            self.dataS_edit.setText('')
                            self.p_edit_2.setText('')
                            self.erro_login.setStyleSheet(
                                "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                            self.error_label.setStyleSheet('color: rgb(102,142,57);')
                            self.error_label.setText('Alteração Bem-Sucedida')
                            self._images = []
                            self._index = 0
                            self._reset_image()
                        except:
                            self.erro_login.setStyleSheet(
                                "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                            self.error_label.setText('Placa Já Cadastrada')
                            return
                    else:
                        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                        self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                        self.error_label.setText('Data de Saída Inválida')
                elif status == 'RETIRADO' and len(data_s) == 0:
                    self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                    self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                    self.error_label.setText('Preencha a Data de Saída')
            else:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                self.error_label.setText('Data de Entrada Inválida')
        else:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Placa Inválida')

    def set_exit_date_visible(self):
        # Altera a visibilidade da caixa de data de saída com base no seletor de status
        if self.status_comboBox.currentIndex() == 0:
            self.dataS_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
                "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
            self.dataS_edit.setPlaceholderText('')
            self.dataS_edit.setText('')
            self.dataS_edit.setReadOnly(True)
        elif self.status_comboBox.currentIndex() == 1:
            self.dataS_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: "
                "5px; background-color: rgb(255,255,255); color: rgb(0,0,0);} QLineEdit:hover{"
                "border: 2px solid rgb(117, 117, 179);} QLineEdit:focus{border: 2px solid rgb("
                "117, 117, 179); color: rgb(40, 40, 40);}")
            self.dataS_edit.setPlaceholderText("Data de Saída")
            self.dataS_edit.setReadOnly(False)


class ConfigWindow(QMainWindow):
    def __init__(self, user):
        super(ConfigWindow, self).__init__()
        loadUi("paginas/ConfigScreen.ui", self)
        self.user = user
        self.assunto_edit.setReadOnly(True)
        self.login_label.setText(self.user.usuario)
        self.name_label.setText(self.user.nome)
        self.surname_label.setText(self.user.sobrenome)
        self.email_label.setText(self.user.email)
        self.back_button.clicked.connect(self.go_back)
        self.edit_button.clicked.connect(self.go_to_change_info)
        self.assunto_checkBox.stateChanged.connect(self.show_subject)
        self.message_checkBox.stateChanged.connect(self.show_message)
        self.emailU_checkBox.stateChanged.connect(self.show_email)
        self.confirm_button.clicked.connect(self.save_configurations)
        self._relatorio_config = None
        self.login_email = ''
        self.password_email = ''
        self._subject_config = ''
        self._message_config = ''
        self._auto_message = """#saudacao,

Segue em anexo #conteudo, referentes ao #nome_do_arquivo

Att"""
        self.get_from_config()

    def show_email(self):
        if self.emailU_checkBox.isChecked():
            self.email_lineEdit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106);border-radius: 5px;padding: 5px;background-color: rgb(79, 79, 79);color: rgb(188, 188, 188);}"
                "QLineEdit:hover{border: 2px solid rgb(117, 117, 179);}")
            self.email_lineEdit.setText(self.user.email)
            self.email_lineEdit.setReadOnly(True)
        else:
            self.email_lineEdit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106);border-radius: 5px;padding: 5px;background-color: #F0F0F0;color: rgb(0,0,0);}"
                "QLineEdit:hover{border: 2px solid rgb(117, 117, 179);}"
                "QLineEdit:focus{border: 2px solid rgb(117, 117, 179);color: rgb(40, 40, 40);}")
            self.email_lineEdit.setText('')
            self.email_lineEdit.setReadOnly(False)

    def show_subject(self):
        if self.assunto_checkBox.isChecked():
            self.assunto_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106);border-radius: 5px;padding: 5px;background-color: rgb(79, 79, 79);color: rgb(188, 188, 188);}"
                "QLineEdit:hover{border: 2px solid rgb(117, 117, 179);}")
            self.assunto_edit.setText('Relatório PLACA ABC1234')
        else:
            self.assunto_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgb(106, 106, 106);border-radius: 5px;padding: 5px;background-color: #F0F0F0;color: rgb(0,0,0);}"
                "QLineEdit:hover{border: 2px solid rgb(117, 117, 179);}"
                "QLineEdit:focus{border: 2px solid rgb(117, 117, 179);color: rgb(40, 40, 40);}")
            self.assunto_edit.setText('')

    def show_message(self):
        if self.message_checkBox.isChecked():
            self._message_config = self.message_textEdit.toPlainText()
            self.message_textEdit.setStyleSheet(
                "QTextEdit{border: 2px solid rgb(106, 106, 106);border-radius: 5px;padding: 5px;background-color: rgb(79, 79, 79);color: rgb(188, 188, 188);}"
                "QTextEdit:hover{border: 2px solid rgb(117, 117, 179);}")
            self.message_textEdit.setReadOnly(True)
            self.message_textEdit.setPlainText(self._auto_message)
        else:
            self.message_textEdit.setStyleSheet(
                "QTextEdit{border: 2px solid rgb(106, 106, 106);border-radius: 5px;padding: 5px;background-color: #F0F0F0;color: rgb(0,0,0);}"
                "QTextEdit:hover{border: 2px solid rgb(117, 117, 179);}"
                "QTextEdit:focus{border: 2px solid rgb(117, 117, 179);color: rgb(40, 40, 40);}")
            self.message_textEdit.setReadOnly(False)
            self.message_textEdit.setPlainText(self._message_config)

    @staticmethod
    def encrypt(message):
        # encription function
        return result_message

    @staticmethod
    def decrypt(message):
        # decription function
        return result_message

    def save_configurations(self):
        # Configurações da mensagem e assunto padrão do email
        self._subject_config = ''
        if self.assunto_checkBox.isChecked():
            self._subject_config = 'mostrar'
        if self.message_checkBox.isChecked():
            self._message_config = self._auto_message
        else:
            self._message_config = self.message_textEdit.toPlainText()
        with open('conexao/email_configurations.txt', 'w') as email_config:
            email_config.write(f"""{self._subject_config}
    /
    {self._message_config}""")
        self._message_config = ''

        # Configuração de ‘login’ e senha do email
        if self.email_lineEdit.text():
            self.login_email = self.email_lineEdit.text()
        if self.senha_lineEdit.text():
            self.password_email = self.encrypt(self.senha_lineEdit.text())

        if self.password_email:
            query_password = f"UPDATE logins SET email_senha = '{self.password_email}' WHERE loginUsuario = '{self.user.usuario}'"
            cur.execute(query_password)
            connection.commit()
        if self.login_email:
            query_email = f"UPDATE logins SET email_login = '{self.login_email}' WHERE loginUsuario='{self.user.usuario}';"
            cur.execute(query_email)
            connection.commit()

        # Configuração de relatório único/múltiplo
        if self.relatorios_checkBox.isChecked():
            self._relatorio_config = '1'
        else:
            self._relatorio_config = '0'

        with open("conexao/config_relatorio.txt", "w") as relatorio_config:
            relatorio_config.write(self._relatorio_config)

        self.erro_login.setStyleSheet(
            "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
        self.error_label.setStyleSheet('color: rgb(102,142,57);')
        self.error_label.setText('Configurações Salvas')

    def get_from_config(self):
        with open('conexao/email_configurations.txt', 'r') as email_config:
            content = email_config.read()
            if '/' in content:
                self._subject_config = content.split('/')[0].strip()
                self._message_config = content.split('/')[1].strip()
        if self._subject_config:
            self.assunto_checkBox.setChecked(True)
        if self._message_config:
            if self._message_config == self._auto_message:
                self.message_checkBox.setChecked(True)
            else:
                self.message_textEdit.setPlainText(self._message_config)

        get_login_query = f"SELECT email_login, email_senha FROM logins WHERE loginUsuario = '{self.user.usuario}'"
        cur.execute(get_login_query)
        login_info = cur.fetchone()
        self.login_email = login_info[0]
        if login_info[1]:
            self.password_email = self.decrypt(login_info[1])
        self.email_lineEdit.setText(self.login_email)
        self.senha_lineEdit.setText(self.password_email)

        with open("conexao/config_relatorio.txt", "r") as relatorio_config:
            content = relatorio_config.read()
            self._relatorio_config = int(content)
        if self._relatorio_config:
            self.relatorios_checkBox.setChecked(True)

    def go_back(self):
        # Retorna para a página principal
        main_page = MainWindow(self.user)
        widget.addWidget(main_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_change_info(self):
        # Vai para a página de alterar informações do usuário
        change_info_page = AlterationConfigScreen(self.user)
        widget.addWidget(change_info_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AlterationConfigScreen(QMainWindow):
    def __init__(self, user):
        super(AlterationConfigScreen, self).__init__()
        loadUi("paginas/AlterationConfigScreen.ui", self)
        self.user = user
        # Deixa os campos de Senha invisíveis
        self.currentPassword_edit.setStyleSheet(
            "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
            "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
        self.currentPassword_edit.setPlaceholderText('')
        self.currentPassword_edit.setReadOnly(True)

        self.newPassword_edit.setStyleSheet(
            "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
            "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
        self.newPassword_edit.setPlaceholderText('')
        self.newPassword_edit.setReadOnly(True)

        self.confirmNewPassword_edit.setStyleSheet(
            "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
            "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
        self.confirmNewPassword_edit.setPlaceholderText('')
        self.confirmNewPassword_edit.setReadOnly(True)
        self.changeInfo_button.clicked.connect(self.change_info)
        self.password_checkBox.stateChanged.connect(self.check_box_changed_action)
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        # Retorna para a página principal
        main_page = ConfigWindow(self.user)
        widget.addWidget(main_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def check_box_changed_action(self):
        if self.password_checkBox.isChecked() is False:
            self.currentPassword_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
                "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
            self.currentPassword_edit.setPlaceholderText('')
            self.currentPassword_edit.setReadOnly(True)

            self.newPassword_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
                "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
            self.newPassword_edit.setPlaceholderText('')
            self.newPassword_edit.setReadOnly(True)

            self.confirmNewPassword_edit.setStyleSheet(
                "QLineEdit{border: 2px solid rgba(106, 106, 106,0); border-radius: 5px; padding: 5px; "
                "background-color: rgba(255,255,255,0); color: rgba(0,0,0,0);}")
            self.confirmNewPassword_edit.setPlaceholderText('')
            self.confirmNewPassword_edit.setReadOnly(True)

        elif self.password_checkBox.isChecked() is True:
            self.currentPassword_edit.setStyleSheet(
                "QLineEdit{    border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: 5px;    background-color: rgb(255,255,255);    color: rgb(0,0,0);}"
                "QLineEdit:hover{border: 2px solid rgb(117, 117, 179);}"
                "QLineEdit:focus{border: 2px solid rgb(117, 117, 179); color: rgb(40, 40, 40);}")
            self.currentPassword_edit.setPlaceholderText('Senha Atual')
            self.currentPassword_edit.setReadOnly(False)

            self.newPassword_edit.setStyleSheet(
                "QLineEdit{    border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: 5px;    background-color: rgb(255,255,255);    color: rgb(0,0,0);}"
                "QLineEdit:hover{border: 2px solid rgb(117, 117, 179);}"
                "QLineEdit:focus{border: 2px solid rgb(117, 117, 179); color: rgb(40, 40, 40);}")
            self.newPassword_edit.setPlaceholderText('Nova Senha')
            self.newPassword_edit.setReadOnly(False)

            self.confirmNewPassword_edit.setStyleSheet(
                "QLineEdit{    border: 2px solid rgb(106, 106, 106); border-radius: 5px; padding: 5px;    background-color: rgb(255,255,255);    color: rgb(0,0,0);}"
                "QLineEdit:hover{border: 2px solid rgb(117, 117, 179);}"
                "QLineEdit:focus{border: 2px solid rgb(117, 117, 179); color: rgb(40, 40, 40);}")
            self.confirmNewPassword_edit.setPlaceholderText('Confirme a Nova Senha')
            self.confirmNewPassword_edit.setReadOnly(False)

    def change_info(self):
        # Altera as informações do usuário no SQL, mantendo iguais os campos em branco
        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 0); border-radius: 10px;")
        self.error_label.setText('')
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        email = self.email_edit.text()
        password = self.currentPassword_edit.text()
        new_password = self.newPassword_edit.text()
        confirm_new_password = self.confirmNewPassword_edit.text()
        if name == '':
            name = self.user.nome
        if surname == '':
            surname = self.user.sobrenome
        if email == '':
            email = self.user.email
        try:
            if '@' in email:
                query_alter = f"UPDATE  logins SET nome = '{name}', sobrenome = '{surname}', email = '{email}' WHERE loginUsuario='{self.user.usuario}';"
                cur.execute(query_alter)
                connection.commit()
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(102,142,57);')
                self.error_label.setText('Alteração Bem-Sucedida')
            else:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                self.error_label.setText('E-mail Inválido')

            if self.password_checkBox.isChecked() is True:
                if password == '':
                    self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                    self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                    self.error_label.setText('Insira a Senha Atual')
                    return
                query = f"SELECT * FROM logins WHERE loginUsuario = '{self.user.usuario}' and pwdcompare('{password}', senhaUsuario) = 1"
                cur.execute(query)
                user = cur.fetchone()[1]
                if user == self.user.usuario:
                    if new_password != '' and confirm_new_password != '':
                        if new_password == confirm_new_password:
                            query_alter = f"DECLARE @novasenha NVARCHAR(256) = '{new_password}' UPDATE logins SET senhaUsuario = (CONVERT(VARBINARY(256),PWDENCRYPT(@novasenha))) WHERE loginUsuario = '{self.user.usuario}'"
                            cur.execute(query_alter)
                            connection.commit()
                            self.erro_login.setStyleSheet(
                                "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                            self.error_label.setStyleSheet('color: rgb(102,142,57);')
                            self.error_label.setText('Alteração Bem-Sucedida')
                        else:
                            self.erro_login.setStyleSheet(
                                "background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                            self.error_label.setText('As Senhas não Conferem')
                            self.newPassword_edit.setText('')
                            self.confirmNewPassword_edit.setText('')
                    else:
                        self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                        self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                        self.error_label.setText('Preencha Todos os Campos')
                else:
                    self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                    self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                    self.error_label.setText('Insira a Senha Atual Correta')
                    self.currentPassword_edit.setText('')
        except:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Insira a Senha Atual Correta')
            self.currentPassword_edit.setText('')


class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        loadUi("paginas/RegisterScreen.ui", self)
        self.register_button.clicked.connect(self.register)
        self.Logout_Button_2.clicked.connect(self.go_to_login)

    @staticmethod
    def go_to_login():
        # Realiza logout e vai pra tela de login
        log_in_page = LoginWindow()
        widget.addWidget(log_in_page)
        try:
            query_remember_user = "SELECT loginUsuario FROM logins WHERE record_User = 1"
            cur.execute(query_remember_user)
            user = cur.fetchone()[0]
            log_in_page.login_edit.setText(user)
            log_in_page.RememberLoginBox.setChecked(True)
        except:
            log_in_page.login_edit.setText('')
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.showMaximized()

    def register(self):
        # Cadastra o usuário no SQL, fazendo diversas verificações
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        login = self.login_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirmpassword_edit.text()
        if len(name) == 0 or len(surname) == 0 or len(login) == 0 or len(email) == 0 or len(password) == 0 or len(
                confirm_password) == 0:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Preencha Todos os Campos')
        elif password != confirm_password:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('As Senhas não Conferem')
        elif '@' not in email:
            self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
            self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
            self.error_label.setText('Insira um Email Válido')
        else:
            try:
                query_register = f"INSERT INTO logins (loginUsuario, senhaUsuario, nome, sobrenome, email) VALUES ('{login}', CONVERT(VARBINARY(256),pwdencrypt('{password}')), '{name}', '{surname}', '{email}')"
                cur.execute(query_register)
                connection.commit()
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(102,142,57);')
                self.error_label.setText('Cadastro Bem-Sucedido')
            except:
                self.erro_login.setStyleSheet("background-color: rgba(195, 195, 195, 1); border-radius: 10px;")
                self.error_label.setStyleSheet('color: rgb(208, 0, 0);')
                self.error_label.setText('Usuário já Cadastrado')


def format_date_from_sql(date):
    # Função para formatar todas as datas vindas do SQL
    date_split = date.split('-')
    year = date_split[0]
    month = date_split[1]
    day = date_split[2]
    return f"{day}/{month}/{year}"


def verify_date(date):
    # Essa função verifica se a data inserida é possível (se não está no futuro, se não tem mais dias
    # do que o mes possui, se o mes não é maior que 12, etc.)
    t = time.localtime()
    day = int(date.split('/')[0])
    month = int(date.split('/')[1])
    year = int(date.split('/')[2])
    current_day = int(time.strftime("%d", t))
    current_month = int(time.strftime("%m", t))
    current_year = int(time.strftime("%Y", t))
    if month > 12:
        return False
    if month == 2:
        if year % 400 == 0 or year % 100 != 0 and year % 4 == 0:
            # Verificação para ano bissexto
            if day > 29:
                return False
        else:
            if day > 28:
                return False
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        if day > 31:
            return False
    elif month in [4, 6, 9, 11]:
        if day > 30:
            return False
    if year > current_year:
        return False
    elif current_year == year:
        if month > current_month:
            return False
        if current_month == month:
            if day > current_day:
                return False
    return True


def days_until(strdate):
    # Essa função verifica se falta menos de um mês para uma data (parâmetro strdate), ou se ela ja passou
    # retorna True para caso tenha passado ou faltem 30 dias, ou False caso falte mais de 30
    days_of_month = None
    date = strdate.split('/')
    due_day = int(date[0])
    due_month = int(date[1])
    due_year = int(date[2])
    t = time.localtime()
    current_day = int(time.strftime("%d", t))
    current_month = int(time.strftime("%m", t))
    current_year = int(time.strftime("%Y", t))

    if current_month in [1, 3, 5, 7, 8, 10, 12]:
        days_of_month = 31
    elif current_month in [4, 6, 9, 11]:
        days_of_month = 30
    elif current_month == 2:
        if current_year % 400 == 0 or current_year % 100 != 0 and current_year % 4 == 0:
            # Verificação para ano bissexto
            days_of_month = 29
        else:
            days_of_month = 28

    if current_year > due_year:
        return True

    elif due_year - current_year == 1:
        if current_month == 12 and due_month == 1:
            days_difference = due_day + (days_of_month - current_day)
            if days_difference <= 30:
                return True

    elif due_year == current_year:
        if due_month - current_month == 1:
            days_difference = due_day + (days_of_month - current_day)
            if days_difference <= 31:
                return True
        elif due_month <= current_month:
            return True
    return False


# Funções para validação de licença


mensagem = validate_license('license.txt')
if mensagem == 'Licença de Uso Vencida':
    with open(fr"conexao/'python3.dll.txt'", "w", encoding='UTF-8') as file_hiddenUsed:
        file_hiddenUsed.write('Licença de Uso Vencida')

with open(r"conexao/connection.txt", "r") as SQL_connection_file:
    # Le o arquivo com os dados da conexão SQL
    file_content = SQL_connection_file.read()

if mensagem != 'Licença de Uso Inválida' and mensagem != 'Licença de Uso Vencida':
    try:
        # Tenta realizar a conexão com o SQL, e emite a mensagem na tela de ‘login’ caso não consiga
        connection_data = ("Driver={SQL Server};" + file_content)
        connection = pyodbc.connect(connection_data)
        cur = connection.cursor()
    except:
        mensagem = "SQL Não Conectado"

position_E_Add = [0]
position_S_Add = [0]
position_E_Alter = [0]
position_S_Alter = [0]

app = QApplication(sys.argv)
widget = QStackedWidget()
logIn_page = LoginWindow()
widget.addWidget(logIn_page)

try:
    query_remember = "SELECT loginUsuario FROM logins WHERE record_User = 1"
    cur.execute(query_remember)
    remembered_user = cur.fetchone()[0]
    logIn_page.login_edit.setText(remembered_user)
    logIn_page.RememberLoginBox.setChecked(True)
except:
    logIn_page.login_edit.setText('')

widget.setMinimumWidth(608)
widget.setMinimumHeight(611)

widget.show()

if days_until(due_date):
    LicenseWarning = LicenceWarningPopUp()
    LicenseWarning.open_license_pop_up()

sys.exit(app.exec_())
