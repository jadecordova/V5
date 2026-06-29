async function HandleImportMovies() {

    const folder = await eel.Select_Folder()();

    // If the user canceled the folder selection.
    if (!Store.SetCurrentFolder(folder)) {

        return;
    }

    const files = await eel.Import_Movies(folder)();
    console.log(files);

}