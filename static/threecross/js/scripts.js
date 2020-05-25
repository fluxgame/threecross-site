function hideCityState() {
	$('#citybox').hide();
	$('#statebox').hide();
	$('#zipbox').addClass("col").removeClass("col-4");	
}

window.setTimeout(function() {
    $("#announcement").fadeTo(500, 0, function(){
        $(this).remove(); 
    });
}, 60000);

$(function() {
$(document).ready( function () {
        $('#mc-embedded-subscribe-form').submit(function (event) {
			$form = $(this);
            event.preventDefault();
            if(! $form.valid()) return false;
		    $.ajax({
	        type: $form.attr('method'),
	        url: $form.attr('action'),
	        data: $form.serialize(),
	        cache       : false,
	        dataType    : 'json',
	        contentType: "application/json; charset=utf-8",
	        error       : function(err) { $("#signup_failed").css("display", "block") },
	        success     : function(data) {
	            if (data.result != "success") {
	                $("#signup_failed").css("display", "block");
	            } else {
					$("#mc_embed_signup").css("display", "none");
	                $("#signup_successful").css("display", "block");
				}
	        }
	    	});
        });
	
        $('#coop-app-form').submit(function (event) {
			$form = $(this);
	        event.preventDefault();

			$form.hide();
			$("#coop_app_processing").show();
			var posting = $.post( $form.attr('action'), $form.serialize());
			
			posting.done(function( data ) {
	            if (data.result != "success") {
	                $("#coop_submit_successful_invoice").hide();
	                $("#coop_submit_successful_no_invoice").hide();
					$("#coop_app_processing").hide();
	                $("#coop_submit_failed").show();
	            } else {
					$("#coop_app_processing").hide();
	                $("#coop_submit_failed").hide();
					if (data.invoice) {
		                $("#coop_submit_successful_invoice").show();
					} else {
		                $("#coop_submit_successful_no_invoice").show();

					}
				}
	        });
			
			posting.fail(function(err) {
				$("#coop_app_processing").hide();
                $("#coop_submit_successful_invoice").hide();
                $("#coop_submit_successful_no_invoice").hide();
				$("#coop_submit_failed").show();
			});
        });
			
	hideCityState();
	
	$('textarea').each(function () {
	  this.setAttribute('style', 'height:' + (this.scrollHeight + 8) + 'px;overflow-y:hidden;');
	}).on('input', function () {
	  this.style.height = 'auto';
	  this.style.height = (this.scrollHeight + 8) + 'px';
	});
	
	$('input[type="tel"]').inputmask("(999) 999-9999");
	
	$('#recaptcha').append($('.grecaptcha-badge')[0]);
	$('.grecaptcha-badge').css("box-shadow", "none").css("margin", "0 auto");
	$('#g-recaptcha-response').hide();	
});
 		
$("#zip").keyup(function() {
				var zip_in = $(this);
				var zip_box = $('#zipbox');
				
				if (zip_in.val().length<5)
				{
					hideCityState();
				}
				else if ( zip_in.val().length>5)
				{
					hideCityState();
					zip_box.addClass('error');
				}
				else if ((zip_in.val().length == 5) ) 
				{
					// Make HTTP Request
					$.ajax({
						url: "https://api.zippopotam.us/us/" + zip_in.val(),
						cache: false,
						dataType: "json",
						type: "GET",
						success: function(result, success) {
							zip_box.addClass("col-4").removeClass("col");	
							$('#citybox').show();
							$('#statebox').show();
				
							places = result['places'][0];
							$("#city").val(places['place name']);
							$("#state").val(places['state abbreviation']);
							zip_box.removeClass('error');
						},
						error: function(result, success) {
							hideCityState();
							zip_box.addClass('error');
						}
					});
				}
	});
});