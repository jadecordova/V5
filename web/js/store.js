class Store {

    static CurrentFolder = null;

    //---------------------------------------------------------------------------------- SetCurrentFolder
    static SetCurrentFolder(folder) {

        if (folder) {
            Store.CurrentFolder = folder;
            return true;
        }

        return false;
    }

}