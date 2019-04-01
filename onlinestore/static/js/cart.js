/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Search
4. Init Menu
5. Init Quantity


******************************/

$(document).ready(function()
{
	"use strict";

	/* 

	1. Vars and Inits

	*/

	var header = $('.header');
	var hambActive = false;
	var menuActive = false;

	setHeader();

	$(window).on('resize', function()
	{
		setHeader();
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	initSearch();
	initMenu();
	initQuantity();
	/* 

	2. Set Header

	*/

	function setHeader()
	{
		if($(window).scrollTop() > 100)
		{
			header.addClass('scrolled');
		}
		else
		{
			header.removeClass('scrolled');
		}
	}

	/* 

	3. Init Search

	*/

	function initSearch()
	{
		if($('.search').length && $('.search_panel').length)
		{
			var search = $('.search');
			var panel = $('.search_panel');

			search.on('click', function()
			{
				panel.toggleClass('active');
			});
		}
	}

	/* 

	4. Init Menu

	*/

	function initMenu()
	{
		if($('.hamburger').length)
		{
			var hamb = $('.hamburger');

			hamb.on('click', function(event)
			{
				event.stopPropagation();

				if(!menuActive)
				{
					openMenu();
					
					$(document).one('click', function cls(e)
					{
						if($(e.target).hasClass('menu_mm'))
						{
							$(document).one('click', cls);
						}
						else
						{
							closeMenu();
						}
					});
				}
				else
				{
					$('.menu').removeClass('active');
					menuActive = false;
				}
			});

			//Handle page menu
			if($('.page_menu_item').length)
			{
				var items = $('.page_menu_item');
				items.each(function()
				{
					var item = $(this);

					item.on('click', function(evt)
					{
						if(item.hasClass('has-children'))
						{
							evt.preventDefault();
							evt.stopPropagation();
							var subItem = item.find('> ul');
						    if(subItem.hasClass('active'))
						    {
						    	subItem.toggleClass('active');
								TweenMax.to(subItem, 0.3, {height:0});
						    }
						    else
						    {
						    	subItem.toggleClass('active');
						    	TweenMax.set(subItem, {height:"auto"});
								TweenMax.from(subItem, 0.3, {height:0});
						    }
						}
						else
						{
							evt.stopPropagation();
						}
					});
				});
			}
		}
	}

	function openMenu()
	{
		var fs = $('.menu');
		fs.addClass('active');
		hambActive = true;
		menuActive = true;
	}

	function closeMenu()
	{
		var fs = $('.menu');
		fs.removeClass('active');
		hambActive = false;
		menuActive = false;
	}

	/* 

	5. Init Quantity

	*/

	function initQuantity()
	{
		// Handle product quantity input
		if($('.product_quantity').length)
		{
			var input = $('#quantity_input');
			var incButton = $('#quantity_inc_button');
			var decButton = $('#quantity_dec_button');

			var originalVal;
			var endVal;

//			incButton.on('click', function()
//			{
//				originalVal = input.val();
//				endVal = parseFloat(originalVal) + 1;
//				input.val(endVal);
////				var price = Number($('.cart_item_price').text());
////				$('.cart_item_total').text(endVal * price);
//			});
//
//			decButton.on('click', function()
//			{
//			    console.log('s')
//				originalVal = input.val();
//				if(originalVal > 0)
//				{
//					endVal = parseFloat(originalVal) - 1;
//					input.val(endVal);
////					var price = Number($('.cart_item_price').text());
////				    $('.cart_item_total').text(endVal * price);
//				}
//			});
		}
	}

});
$('.quantity_change').change(function(){
    $.ajax({
            url:'/ajax/get_number/',
            data:{},
            dataType:'json',
            success: function(data){
                var totalSum = 0;
                for (var i=1; i<=data.number; i++){
                    var key = $('.cart_item_price'+i)
                    var price = key.text();
                    var quantity = $('#quantity_input'+i).val()
                    var total = quantity * price;
                    var primaryKey = key.attr('data-pk');
                    updateItem(primaryKey, quantity);
                    $('.cart_item_total'+i).text(total);
                    totalSum = totalSum + total
                }
                $('#subtotal').text(totalSum);
                $('#total').text(totalSum);
                }
            })
})
    function updateItem(x, y){
        $.ajax({
            url:'/ajax/updatecart/',
            data:{
                'primaryKey':x,
                'quantity':y,
            },
            dataType:'json',

        })
    }
