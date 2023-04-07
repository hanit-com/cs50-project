// MARK: - Constants

const cardsListId = "cards_list";
const noCardsDivlId = "no_cards_div";
const containerIdPrefix = "card_container_";
const contentIdPrefix = "card_content_";
const cardIdPrefix = "card_";
const removeButtonName = "card_remove_button";

// MARK: - Initializations

document.addEventListener("DOMContentLoaded", pageLoaded);

function pageLoaded() {
    loadPageData();
    setListeners();
}

function setListeners() {
    const form = document.getElementById("card_creation_form");
    form.onsubmit = function() { createCard(form); };
}

// MARK: - AJAX Queries

function loadPageData() {
    const collection_id = jQuery.parseJSON($("#collection_data").data("id"));

    $.ajax({
        url : "/cards",
        type: "GET",
        dataType: "JSON",
        data: { "collection_id": collection_id },
        success: function (response) {
            setPageElements(response.cards);
        },
        error: errorHandler
    });
}

function createCard(form) {
    event.preventDefault();
    $.ajax({
        url: "/createCard",
        type: "POST",
        dataType: "JSON",
        data: $(form).serialize(),
        success: function(response) {
            $("#" + noCardsDivlId).hide();
            $("#" + cardsListId).show();

            addCardItem(response.newCard);
            form.reset();
        },
        error: errorHandler
    });
}

function deleteCard(id) {
    $.ajax({
        url: "/deleteCard",
        type: "POST",
        dataType: "JSON",
        data: { "id": id },
        success: function(response) {
            document.getElementById(containerIdPrefix + id).remove();

            if (!$(".card").length) {
                $("#" + noCardsDivlId).show();
                $("#" + cardsListId).hide();
            }
        },
        error: errorHandler
    });
}

// MARK: - Click Events

function cardClicked(cardtId) {
    if(event.target.name == removeButtonName) {
        return;
    }

    const content = document.getElementById(contentIdPrefix + cardtId);
    const card = document.getElementById(cardIdPrefix + cardtId);

    if(content.style.visibility == "visible") {
        content.style.visibility = "hidden";
        $(card).addClass("card-background");
    } else {
        content.style.visibility = "visible";
        $(card).removeClass("card-background");
    }
}

// MARK: - UI

function errorHandler(xhr, status, error) {
    alert(`Error code: ${xhr.status} - ${xhr.responseText}`);
}

function setPageElements(cards) {
    const container = document.getElementById("cards_container");
    const noDataDiv = getNoDataDiv();

    const cardsList = document.createElement("div");
    cardsList.id = cardsListId;

    container.append(noDataDiv);
    container.append(cardsList);

    if (cards.length == 0) {
        $("#" + cardsListId).hide();
        $("#" + noCardsDivlId).show();
    } else {
        $("#" + noCardsDivlId).hide();
        $("#" + cardsListId).show();
    }

    cards.forEach(addCardItem);
}

function addCardItem(card) {
    const cardContainer = document.createElement("div");
    cardContainer.setAttribute("class", "col-md-4 top-buffer container card-container");
    cardContainer.id = containerIdPrefix + card.id;
    cardContainer.onclick = function() { cardClicked(card.id); };

    const cardDiv = getCardDiv(card);
    cardContainer.append(cardDiv);

    const cardsSection = document.getElementById(cardsListId);
    cardsSection.prepend(cardContainer);
}

function getCardDiv(card) {
    const cardDiv = document.createElement("div");
    cardDiv.setAttribute("class", "card card-1");
    $(cardDiv).addClass("card-background");
    cardDiv.id = cardIdPrefix + card.id;

    const topDiv = document.createElement("div");
    const title = getCardTitle(card);
    const content = getCardContent(card);
    const removeButton = getCardRemoveButton(card);

    topDiv.append(removeButton);
    topDiv.append(title);

    cardDiv.append(topDiv);
    cardDiv.append(content);

    return cardDiv;
}

function getNoDataDiv() {
    const noDataDiv = document.createElement("div");
    noDataDiv.id = noCardsDivlId;

    const label = document.createElement("p");
    label.setAttribute("class", "no-data-label");
    label.innerHTML = "No cards in the collection";

    const image = document.createElement("img");
    image.setAttribute("class", "no-data-image");
    image.src = "/static/assets/no_data_found.jpeg";

    noDataDiv.append(label);
    noDataDiv.append(image);

    return noDataDiv;
}

function getCardContent(card) {
    const content = document.createElement("p");
    content.setAttribute("class", "card-content");
    content.id = contentIdPrefix + card.id;
    const text = card.content.replace(/(?:\r\n|\r|\n)/g, "<br>");
    content.innerHTML = text;

    return content;
}

function getCardRemoveButton(card) {
    const removeButton = document.createElement("button");
    removeButton.setAttribute("class", "btn btn-outline-light delete-button inline card-remove-button");
    removeButton.onclick = function() { deleteCard(card.id); };
    removeButton.name = removeButtonName;
    removeButton.innerHTML = "X";

    return removeButton;
}

function getCardTitle(card) {
    const title = document.createElement("h4");
    title.setAttribute("class", "card-title");
    title.innerHTML = card.title;

    return title;
}