from app.views.notas_view import InterfazNotas
from app.controllers.notas_controller import NotasController


def main():
    # Inicializa la vista sin controlador
    view = InterfazNotas(None)
    # Inicializa el controlador con la vista
    controller = NotasController(view)
    # Asigna el controlador a la vista si existe el atributo
    if hasattr(view, 'controller'):
        view.controller = controller
    # Lanza la UI principal (Tkinter root o método run)
    if hasattr(view, 'root') and hasattr(view.root, 'mainloop'):
        view.root.mainloop()
    elif hasattr(view, 'run'):
        view.run()
    else:
        print('No se encontró método para lanzar la UI')

if __name__ == '__main__':
    main()
