import flet as ft
from time import sleep


class SaveSelectFile(ft.Row):
    def __init__(self, tipo = 'path'):
        '''
        tipo  == path: seleciona uma pasta (retorna o caminho completo da pasta selecionada)
        tipo  == file: seleciona um arquivo (retorna o caminho completo do arquivo selecionado)
        tipo  == save: sala um arquivo (retorna o caminho completo do arquivo, junto com seu nome)
        
        '''        
        super().__init__()
        self.tipo = tipo
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.selected_files = ft.Text()
        self.nome_arquivo = None
        # self.func = None



        if tipo == 'file':
            self.controls = [
                ft.ElevatedButton(
                    "Selecionar Arquivo",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=self.Select,
                ),
                self.selected_files,
            ]
        elif tipo == 'path':
            self.controls = [
                ft.ElevatedButton(
                    "Selecionar Pasta",
                    icon=ft.icons.FOLDER,
                    on_click=self.Select_pasta,
                ),
                self.selected_files,
            ]   
        elif tipo == 'save':
            self.controls = [
                ft.ElevatedButton(
                    "Salvar",
                    icon=ft.icons.SAVE,
                    on_click=self.Save,
                ),
                self.selected_files,
            ]                      


    def pick_files_result(self, e: ft.FilePickerResultEvent):
        match self.tipo:
            case 'file':
                self.nome_arquivo = f'{e.files[0].path}'
            case 'save':
                self.nome_arquivo = f'{e.path}.{self.tipo}'
            case 'path':
                self.nome_arquivo = f'{e.path}'

        self.selected_files.value = self.nome_arquivo
        self.selected_files.update()
        super().update()

        
    # @property
    def Save(self,e):
        self.pick_files_dialog.save_file() #file_type = ft.FilePickerFileType.CUSTOM, allowed_extensions = [self.tipo]
        while not self.nome_arquivo:
            sleep(0.3)
        self.update()
        return self.nome_arquivo
    
    def Select(self, e):
        self.pick_files_dialog.pick_files(allow_multiple=True)
        while self.nome_arquivo == None:
            sleep(0.3)
        self.update()
        return self.nome_arquivo  

    def Select_pasta(self,e):        
        self.pick_files_dialog.get_directory_path(dialog_title = 'selecione a pasta')
        while not self.nome_arquivo:
            sleep(0.3)
        self.update()
        return self.nome_arquivo            
    
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()

    # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    def will_unmount(self):
        self.page.overlay.remove(self.pick_files_dialog)
        self.page.update()    
 

def main(page: ft.Page):
    page.window_width = 400  # Define a largura da janela como 800 pixels
    page.window_height = 300  #    
    page.title = "Baixar vídeos do Youtube"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
    url_field = ft.TextField(hint_text="Insira a URL do vídeo aqui", width=300, border_color = 'white,0.8')
    download_button = ft.ElevatedButton("Baixar", 
                                        # on_click=lambda e: baixar_video(url_field.value)
                                        )
    select_button = SaveSelectFile('path')
    mp3 = ft.Checkbox(label = 'Converter para mp3?', value = False)
    output = ft.Text("")

    page.add(
        ft.Column(
            [
                url_field,
                select_button,                
                ft.Row([download_button,mp3]),
                ft.Column([output],auto_scroll = True, scroll=ft.ScrollMode.ADAPTIVE, height=70)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    


ft.app(main, 
       view = ft.AppView.WEB_BROWSER,
       route_url_strategy="hash"
         )
