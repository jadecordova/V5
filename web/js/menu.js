class Menu {

    static GetMenuItems() {
        Menu.ImportMoviesButton = document.getElementById('import-movies-menu-button');
        Menu.AddStarButton = document.getElementById('add-star-menu-button');
        Menu.AddTagButton = document.getElementById('add-tag-menu-button');
    }

    static InitImportMoviesButton() {
        Menu.ImportMoviesButton.addEventListener('click', e => {
            HandleImportMovies();
        });
    }

    static Init() {
        Menu.GetMenuItems();
        Menu.InitImportMoviesButton();
    }
}