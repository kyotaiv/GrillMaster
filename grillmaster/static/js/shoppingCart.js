function increaseAmount() {
    $('#amount').text(function (i, oldText) {
        let currentAmount = parseInt(oldText);
        return ++currentAmount; 
    });
}

function decreaseAmount() {
    $('#amount').text(function (i, oldText) {
        let currentAmount = parseInt(oldText);
        return --currentAmount; 
    });
}

function textToPrice(text) {
    text = text
        .substr(1, text.length)
        .split('.')
        .join('');
    return parseInt(text);
}

function addProductToCart(product) {
    $('#shoppingList').append(`
        <tr>
            <td class="w-25">
                <img src="${product.img}" class="img-fluid img-thumbnail" alt="Sheep">
            </td>
            <td>${product.title} - ${product.description}</td>
            <td>$ <span class="shoppingCartItemPrice">${product.price}</span></td>
            <td>
                <button class="btn btn-danger btn-sm remove-product">
                    <i class="fa fa-times"></i>
                </button>
            </td>
        </tr>
    `);

    $('#shoppingList tr').last().find('.remove-product').click(function(event) {
        const parent = $(event.currentTarget).parent().parent();
        const priceRemovedItem = parseInt(parent.find('.shoppingCartItemPrice').text());
        const total = parseInt($('#shoppingCartTotal').text()) - priceRemovedItem;
        $('#shoppingCartTotal').text(total);
        parent.remove();
        decreaseAmount();
    });
    const total = parseInt($('#shoppingCartTotal').text()) + product.price;
    $('#shoppingCartTotal').text(total);
}

$(document).ready(function() {
    $('#cartButton').click(function() {
        $('#cartModal').modal('show');
    });
    $('.add-product').click(function(event) {
        const parent = $(event.currentTarget).parent();
        const title = parent.find('h5').text();
        const description = parent.find('p').text();
        const img = parent.parent().find('img').attr('src');
        const price = textToPrice(parent.find('h3').text());
        addProductToCart({
            title,
            description,
            price,
            img,
        });
        increaseAmount();
    });
});