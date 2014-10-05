var fadeItem = 0;

	$('.container').isotope({
		
		layoutMode: 'masonry',
		masonry: {
			columnWidth: $('.container').width() / 2
		},
		animationEngine : 'jquery',
		itemSelector : '.widget'
		
	});
$(document).ready(function() {
		
	$('.feed li').bind({
		mouseenter:function() {
			
			$(this).css({'border-color':'#1E7EC8'});
			
		},mouseleave:function() {
			
			
			$(this).css({'border-color':'#D9D9D9'});
		}
		
	});
	
	
	updateHeight();
	
	setTimeout(startFade,400);
		
});

function startFade () {
	
	$('.widget:eq('+fadeItem+')').fadeIn();
	
	if (fadeItem < 4) {
	
		fadeItem++;
	
		setTimeout(startFade,600);
	}
}

$(window).resize(function() {
	updateHeight();
});

function updateHeight() {
	
	
	var widgetWidth;
	
	if ($('body').width() > 1100) {
		
		widgetWidth = ($('body').width() - 70)/2;
		
		$('.container').isotope( 'option', { masonry: {columnWidth: $('.container').width() / 2} } );
	
	} else {
		
		widgetWidth = ($('body').width() - 40);
		
		$('.container').isotope( 'option', { masonry: {columnWidth: $('.container').width()}  } );
		
	}
	
	$('.widget').css("width",widgetWidth+"px");
	
	if ($('body').width() > 800) {
		
		$('.sidebar').css("top",70+"px");
		$('.twitter').css("margin-bottom",30+"px");
	
	} else {
		
		$('.sidebar').css("top",135+"px");
		$('.twitter').css("margin-bottom",20+"px");
		
	}
	
	gapi.plus.render('badge',  {"href": "https://plus.google.com/108855452729844077920", "width": "293", "height": "131", "theme": "light"});
	
	$('.container').isotope('reLayout');

}