$(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

$(document).ready(function() {

	$("input, textarea").placeholder();

	$("form").show();

	// bouton scroll top
	$('#btn_up').on("click", function(e) {
		e.preventDefault();
		$('html,body').animate({scrollTop: 0}, 'slow');
	});

	$(window).scroll(function(){
		if($(window).scrollTop()<50){
			$('#btn_up').fadeOut();
		}else{
			$('#btn_up').fadeIn();
		}
	});

});
