async function deleteSchema(element){
//    let request = new XMLHttpRequest();
//    console.log(this)
//    console.log(this.value)
    let i = this.value;
//    request.open("DELETE", "http://localhost:8000/api/edit_detail/" + i + '/');
//    request.send();
//

    const response = await fetch("http://localhost:8000/api/edit_detail/" + i + '/', {
        method: 'DELETE',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',

    })
//    request.onload = () => {
////        window.location.reload(false);
////        hideUserFields();
////        updateTable();
//    }


}
//document.getElementById("add-column").addEventListener("click", createRow);
let danger_links = document.getElementsByClassName("danger-link");
for (let c of danger_links){
    c.addEventListener("click", deleteSchema);
}