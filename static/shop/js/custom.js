$(document).ready(function(){
    // alert(' ');
    let pageName = $('.page-name').attr('page-value');

    //  for adding to cart
    if(localStorage.getItem('cart') == null){
        cart = {};
    }else{
        cart = JSON.parse(localStorage.getItem('cart'));

        document.getElementById('cart').innerHTML = Object.keys(cart).length;
    }

    $('#popcart').popover();
    updtPopover(cart);

    if(pageName == 'home'){
        $('.add-to-cart').click(function(){
            $(this).text('Added to Cart').attr('disabled', true);
            let idstr = this.id.toString();

            if(cart[idstr] != undefined){
                console.log(cart);
                cart[idstr]['qty'] = cart[idstr]['qty']+1;
            }else{
                itemName = $(this).siblings('.prod-name').text();
                itemPrice = $(this).siblings('.prod-price').text();
                itemDesc = $(this).siblings('.prod-desc').text();
                itemImage = $(this).parent().siblings('.prod-image').attr('src');
                cart[idstr] = {};
                cart[idstr]['qty'] = 1;
                cart[idstr]['name'] = itemName;
                cart[idstr]['price'] = itemPrice;
                cart[idstr]['desc'] = itemDesc;
                cart[idstr]['image'] = itemImage;
            }
            localStorage.setItem('cart', JSON.stringify(cart));
            document.getElementById('cart').innerHTML = Object.keys(cart).length;
            if(cart){updtPopover(cart);}
        });
    }

    if(pageName == 'contact'){
        /*code goes for contact page */
        /*for submit form*/
        CKEDITOR.replace( 'msg' );
        $('.contact-submit').on('click', function(e){
            e.preventDefault();
            let formdata = new FormData($('#contact-form')[0]);
            formdata.append('message', CKEDITOR.instances['msg_field'].getData());
            $.ajax({
                url: window.location.href,
                data: formdata,
                type: 'post',
                contentType: false,
                processData: false,
                success: function(response){
                    if(response.success){
                        let msg = '<strong>Success! </strong>'+response.msg;
                        $('.contact-submit-alert').prepend(msg).show().delay(3000).fadeOut( "slow");
                    }
                }
            });
        });
    }

    if(pageName == 'checkout'){
        let cart = JSON.parse(localStorage.getItem('cart'));
        console.log(cart);
        updtChkoutPage(cart);
        $(document).on('click', '.chkout-remove-item', function(){
            let prodId = $(this).attr('prod-id');
            if(delete cart[prodId]){
                localStorage.setItem('cart', JSON.stringify(cart));
                document.getElementById('cart').innerHTML = Object.keys(cart).length;
                updtChkoutPage(cart);
                updtPopover(cart);
            }
        });

        $(document).on('click', '.modify-checkout-item-qty', function(){
            let updtQty = $(this).attr('data-value');
            let exstQty = $(this).siblings('.item-qty').val();
            let prodId = $(this).attr('prod-id');
            let cart = JSON.parse(localStorage.getItem('cart'));
            let new_qty = parseInt(exstQty) + parseInt(updtQty);
            if(new_qty < 1 ) new_qty = 1;
            cart[prodId].qty = new_qty;
            localStorage.setItem('cart', JSON.stringify(cart));
            $(this).siblings('.item-qty').val(new_qty);
            let subtotal = parseInt(cart[prodId].price.match(/(\d+)/)[0]) * new_qty;
            $(this).parents('td').siblings('.subtotal').html('$'+subtotal);
            let totalCheckout = 0;
            $.each(cart, function(i,v){
                let subtotal = parseInt(v.price.match(/(\d+)/)[0]) * v.qty;
                totalCheckout += subtotal;
            });
            $('.total-checkout').html('Total $'+totalCheckout);
        });

        $(document).on('click', '#checkout-modal-open', function(){
            console.log(JSON.stringify(cart));
            $('#total-checkout-items').val(JSON.stringify(cart));
        });
    }

    $(document).on('click', '.remove-popover-cart-item', function() {
        let prodId = $(this).attr('prod-id');
        let prodPrice = $(this).parent().siblings('.popoverProdPrice').html();
        prodPrice = parseInt(prodPrice.match(/(\d+)/)[0]);
        let totalPrice = $('.popoverTotalPrice').html();
        totalPrice = parseInt(totalPrice.match(/(\d+)/)[0]);
        totalPrice -= prodPrice;
        if(delete cart[prodId]){
            localStorage.setItem('cart', JSON.stringify(cart));
            document.getElementById('cart').innerHTML = Object.keys(cart).length;
            $('#'+prodId).attr('disabled', false);
            if(Object.keys(cart).length > 0){
                $(this).parents('.row').remove();
                $('.popoverTotalPrice').html('$'+totalPrice);
                updtPopover(cart);
            }else{
                $('[data-original-title]').popover('hide');
                $('#popcart').attr('data-content','Cart is empty.');
            }
        }else{
            alert('Item doesn\'t exist.');
        }
    });

    function updtPopover(cart){

        if(Object.keys(cart).length > 0){
            let itemsHtml = '';
            let totalPrice = 0;
            $.each(cart, function(i,v){
                itemName = v.name;
                itemPrice = v.price;
                totalPrice += parseInt(itemPrice.match(/(\d+)/)[0]);
                itemsHtml += '<div class="row"><div class="col-7">'+itemName+'</div><div class="col-3 popoverProdPrice">'+itemPrice+'</div><div class="col-2"><a href="javascript:void(0)" style="color:red" class="remove-popover-cart-item" prod-id="'+i+'"><i class="fa fa-times-circle-o"></i></a></div></div>';
                $('#'+i).text('Added to Cart').attr('disabled', true);
            });
            let headingHtml = '<h6>Carts for your item in my shopping cart: </h6>';
            let totalPriceHtml = '<hr><div class="row"><div class="col-md-8 font-weight-bold text-right">Total:</div><div class="col-md-4 font-weight-bold popoverTotalPrice">$'+totalPrice+'</div></div>';
            let checkoutBtnHtml = '<a href="/shop/checkout" class="btn btn-success btn-lg btn-block">Checkout</a>';
            let popoverHtml = headingHtml+itemsHtml+totalPriceHtml+checkoutBtnHtml;
            $('#popcart').attr('data-content',popoverHtml);
        }
    }

    function updtChkoutPage(cart){
        let itemsHtml = '';
        let totalCheckout = 0;
        $.each(cart, function(i,v){
        let subtotal = parseInt(v.price.match(/(\d+)/)[0]) * v.qty;
        totalCheckout += subtotal;
        itemsHtml += `<tr>
            <td data-th="Product">
                <div class="row">
                    <div class="col-sm-3 hidden-xs"><img src="${v.image}" alt="..." class="checkout-prod-img" /></div>
                    <div class="col-sm-9">
                        <h4 class="nomargin">${v.name}</h4>
                        <p>${v.desc}</p>
                    </div>
                </div>
            </td>
            <td data-th="Price">${v.price}</td>
            <td data-th="Quantity">
                <div class="counter">
                  <button class="btn btn-outline-dark  dec modify-checkout-item-qty" data-value="-1" prod-id="${i}" ><i class="fa fa-minus-circle"></i></button>
                  <input class="item-qty" value="${v.qty}" disabled="disabled"/>
                  <button class="btn btn-outline-dark inc modify-checkout-item-qty" data-value="+1" prod-id="${i}" ><i class="fa fa-plus-circle"></i></button>
                </div>
            </td>
            <td data-th="Subtotal" class="text-center subtotal">$${subtotal}</td>
            <td class="actions" data-th="">
                <button class="btn btn-info btn-sm"><i class="fa fa-refresh"></i></button>
                <button prod-id="${i}" class="btn btn-danger btn-sm chkout-remove-item"><i class="fa fa-trash-o"></i></button>
            </td>
        </tr>`;
        });
        $('#checkout-items').html(itemsHtml);
        $('.total-checkout').html('Total $'+totalCheckout);
    }


    //for closing popover onclick outside...
    $('html').on('click', function(e) {
        if (!(typeof $(e.target).data('original-title') != 'undefined' || typeof $(e.target).parents('#popcart').data('original-title') != 'undefined')) {
            $('[data-original-title]').popover('hide');
        }
    });
});

//form validation
(function () {
  'use strict'

  window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation')

    // Loop over them and prevent submission
    Array.prototype.filter.call(forms, function (form) {
      form.addEventListener('submit', function (event) {
        if (form.checkValidity() === false) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })
  }, false)
}())

