// MARK: - Constants
const collectionsListId = "collections_list";
const noCollectionsDivId = "no_collections_div";

// MARK: - Initializations

document.addEventListener("DOMContentLoaded", pageLoaded);

function pageLoaded() {
    loadPageData();
    setListeners();
}

function setListeners() {
    const form = document.getElementById("collection_form");
    form.onsubmit = function() { createCollection(form); };
}

// MARK: - AJAX Queries

function loadPageData() {
    $.ajax({
        url : "/collections",
        type: "GET",
        dataType: "JSON",
        success: function (response) {
            setPageElements(response.collections);
        },
        error: errorHandler
    });
}

function createCollection(form) {
    event.preventDefault();
    $.ajax({
        url: "/createCollection",
        type: "POST",
        dataType: "JSON",
        data: $(form).serialize(),
        success: function(response) {
            $("#" + noCollectionsDivId).hide();
            $("#" + collectionsListId).show();

            addCollectionItem(response.newCollection);
            form.reset();
        },
        error: errorHandler
    });
}

function deleteCollection(id, name) {
    const isConfirmed = confirm(`Are you sure you want to delete the collection \"${name}\"?`);

    if (!isConfirmed) {
        return;
    }

    $.ajax({
        url : "/deleteCollection",
        type: "POST",
        dataType: "JSON",
        data : { "id": id },
        success: function () {
            document.getElementById("li_" + id).remove();

            if (!$(".collections-li").length) {
                $("#" + noCollectionsDivId).show();
                $("#" + collectionsListId).hide();
            }
        },
        error: errorHandler
    });
}

// MARK: - Click Events

function collectionClicked(collectionId) {
    if(event.target.name == "delete_collection_button") {
        return;
    }

    window.location.href = "/collection?id=" + collectionId
}

// MARK: - UI

function errorHandler(xhr, status, error) {
    alert(`Error code: ${xhr.status} - ${xhr.responseText}`);
}

function setPageElements(collections) {
    const container = document.getElementById("collections_container");

    const noDataDiv = getNoDataDiv()

    const ul = document.createElement("ul");
    ul.setAttribute("class", "collections-ul");
    ul.id = collectionsListId;

    container.append(noDataDiv);
    container.append(ul);

    if (collections.length == 0) {
        $("#" + collectionsListId).hide();
        $("#" + noCollectionsDivId).show();
    } else {
        $("#" + noCollectionsDivId).hide();
        $("#" + collectionsListId).show();
    }

    collections.forEach(addCollectionItem);
}

function getNoDataDiv() {
    const noDataDiv = document.createElement("div");
    noDataDiv.id = noCollectionsDivId;

    const label = document.createElement("p");
    label.setAttribute("class", "no-data-label");
    label.innerHTML = "No collections";

    const image = document.createElement("img");
    image.setAttribute("class", "no-data-image");
    image.src = "/static/assets/no_data_found.jpeg";

    noDataDiv.append(label);
    noDataDiv.append(image);

    return noDataDiv;
}

function addCollectionItem(collection) {
    const li = getCollectionLi(collection);
    const button = getCollectionRemoveButton(collection);
    const ul = document.getElementById(collectionsListId);

    li.append(button);
    ul.prepend(li);
}

function getCollectionLi(collection) {
    const li = document.createElement("li");collection-li
    li.setAttribute("class", "list-group-item list-group-item-action collections-li");
    li.innerHTML = collection.name;
    li.onclick = function() { collectionClicked(collection.id); };
    li.id = "li_" + collection.id;

    return li;
}

function getCollectionRemoveButton(collection) {
    const button = document.createElement("button");
    button.innerHTML = "x";
    button.name = "delete_collection_button";
    button.setAttribute("class", "btn btn-outline-light collection-remove-button remove-collection");
    button.onclick = function() { deleteCollection(collection.id, collection.name) };

    return button;
}