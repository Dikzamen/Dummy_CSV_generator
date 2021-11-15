function hideRange(dataRow, visible){
    let value;
    if (visible === true){
        value = 'visible';
    }
    else{
        value = 'hidden';
    }
    let inputFields = dataRow.getElementsByClassName("table-cell-range");
    let labelFields = getLabelRow(dataRow).getElementsByClassName("table-cell-range");
    for (let i = 0; i < labelFields.length; i += 1){
        inputFields[i].style.visibility = value;
        labelFields[i].style.visibility = value;
    }
}

function changeRole(selector){
    if (selector.tagName !== "SELECT"){
        selector = this;
    }
    if (selector.value === "Integer" || selector.value === "Text"){
        hideRange(selector.parentElement.parentElement, true);
    }
    else{
        hideRange(selector.parentElement.parentElement, false);
    }
}

function listenerForSelectors(){
    let selectors = document.getElementsByClassName("select-type");
    for (const selector of selectors) {
        selector.addEventListener("change", changeRole);
    }
}

function deleteRow(){
    let dataRow = this.parentElement.parentElement.parentElement;
    if (dataRow.parentElement.parentElement.id === 'new-columns'){
        return;
    }
    let table = dataRow.parentElement;
    let labelRow = getLabelRow(dataRow);
    if (labelRow === null){
        return;
    }
    labelRow.remove();
    dataRow.remove();

}

function getLabelRow(dataRow){
    let table = dataRow.parentElement;
    for (let i = 0; i < table.children.length; i += 1){
        if (table.children[i] === dataRow){
            return table.children[i-1];
        }
    }
    return null;
}

function listenerForDelete(){
    let selectors = document.getElementsByClassName("delete-button");
    for (const selector of selectors) {
        selector.addEventListener("click", deleteRow);
    }
}

listenerForSelectors();

function createRow(){
    let table = document.getElementById("schema-table");
    let parent = this.parentElement;
    let rows = parent.getElementsByTagName("tr");
    let clone;
    for (const row of rows) {
        clone = row.cloneNode(true);
        if (row.classList.contains("input_row")){
            clone.children[1].children[0].value = row.children[1].children[0].value;
        }
        table.appendChild(clone);
    }
    listenerForSelectors();
    listenerForDelete();
}

function getFormData(){
    let title = document.getElementById("form-title").value;
    let separator = document.getElementById("form-separator").value;
    let character = document.getElementById("form-character").value;
    let user = document.getElementById("userId").value;
    let form = document.getElementById("schema-table");
    data = {};
    data['title'] = title;
    data['column_separator'] = separator;
    data['string_character'] = character;
    data['user'] = user;

    let json_dict = {};
    let row;
    let item;
    let input_el;
    let items = [];
    for(let row_num = 0; row_num < form.childElementCount; row_num++){
        row = form.children[row_num];
        item = {}
        if (row.classList[0] !== "input_row") continue;
        for(let element of row.children){
            if (element.childElementCount === 0) continue;
            if (element.children[0].tagName === "INPUT" || element.children[0].tagName === "SELECT"){
                input_el = element.children[0];
                item[input_el.getAttribute("name")] = input_el.value;
            }

        }
        items.push(item);
    }
    data['items'] = items;
    return data;
}

async function request(){
    let data = getFormData();
    let request_url = api_url;
    let method = api_method;
    let response = await fetch(request_url, {
        method: method,
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
    let json = await response.json();
    if (response.status > 399){
        document.getElementById("errors_json").innerHTML = JSON.stringify(json);
    }
    else{
        window.location.href = redirect_url;
    }
}

function onLoad(type){
    let selectors = document.getElementsByClassName("select-type");
    for (const selector of selectors) {
        changeRole(selector);
    }
    let deleteButtons = document.getElementsByClassName("delete-button")
    for (const button of deleteButtons){
        button.addEventListener("click", deleteRow);

    }
    document.getElementById("submit_button").addEventListener("click", request);
}
let title = "{{ schema.title }}";
document.getElementById("add-column").addEventListener("click", createRow);

