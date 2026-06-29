eel.expose(ShowProgressDialog);
function ShowProgressDialog() {
    console.log('Progress called');
}

eel.expose(UpdateProgress);
function UpdateProgress(current, total) {
    console.log(`${current}/${total}`);
}