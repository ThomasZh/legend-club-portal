/*
 Theme Name: Quick Travel
 Theme URL: http://nasfactor.com/themes/quicktravel/
 Author: NasirWd
 Author URI: www.nasfactor.com
 Description: QuickTravel Unbounce Landing page is best suitable for Travel Agency’s / Travel Agents offering special tourism packages to exotic locations
 Version: 1.0.0
 */

//=======================================================
// Banner
//=======================================================
(function($) {
    'use strict';
    getWidthAndHeight();
    $(window).resize(function() {
        getWidthAndHeight();
    });
    function getWidthAndHeight() {
        var winWidth = $(window).width();
        var winHeight = $(window).height();
        var slheight = $(".slContent").height();
        var slPad = (winHeight - slheight) / 2;
        $('.banners').css({'height': winHeight});
        $('.slContent').css({'padding-top': slPad});
    }

    //=========================
    //Testmonial Carowsel
    //=========================
    $("#testCaro").owlCarousel({
        items: 1,
        dots: true
    });


    //=======================================================
    // Video Section
    //=======================================================
    var vid1 = document.getElementById("myVideo1");
    vid1.play();
    function playPause1() {
        if (vid1.paused) {
            vid1.play();
        } else {
            vid1.pause();
        }
    }
    if ($("#videoWrap1").length > 0)
    {
        $('#playVideos').on('click', function(e) {
            e.preventDefault();
            playPause1();
            if ($(this).hasClass('active'))
            {
                $(this).removeClass('active');
                vid1.pause();
            } else
            {
                $(this).addClass('active');
                vid1.play();
            }
        });
    }
    ;

    //=======================================================
    // Google map
    //=======================================================
    if ($('#map').length > 0) {
        var map;
        map = new GMaps({
            el: '#map',
            lat: -17.818110,
            lng: 178.012453,
            zoomControlOpt: {
                style: 'SMALL',
                position: 'TOP_LEFT'
            },
            scrollwheel: false,
            zoom: 8,
            zoomControl: false,
            panControl: false,
            streetViewControl: false,
            mapTypeControl: false,
            overviewMapControl: false,
            clickable: false
        });
        map.addMarker({
            lat: -17.818110,
            lng: 178.012453,
            icon: 'images/marker.png',
            animation: google.maps.Animation.DROP,
            verticalAlign: 'bottom',
            horizontalAlign: 'center',
            backgroundColor: '#d3cfcf'
        });


        var styles = [
            {
                "featureType": "road",
                "stylers": [
                    {"color": "#ffffff"}
                ]
            }, {
                "featureType": "water",
                "stylers": [
                    {"color": "#74c3ff"}
                ]
            }, {
                "featureType": "landscape",
                "stylers": [
                    {"color": "#ffffff"}
                ]
            }, {
                "elementType": "labels.text.fill",
                "stylers": [
                    {"color": "#2d2d2d"}
                ]
            }, {
                "featureType": "poi",
                "stylers": [
                    {"color": "#ffffff"}
                ]
            }, {
                "elementType": "labels.text",
                "stylers": [
                    {"saturation": 1},
                    {"weight": 0.1},
                    {"color": "#ffffff"},
                    {"visibility": "off"}
                ]
            }

        ];



        map.addStyle({
            styledMapName: "Styled Map",
            styles: styles,
            mapTypeId: "map_style"
        });

        map.setStyle("map_style");
    }

    //========================
    // Mobile Menu
    //========================
    if ($('.mobileMenu').length > 0) {
        $('.mobileMenu').on('click', function() {
            $(this).toggleClass('active');
            $('.mainNav > ul').slideToggle('slow');
        });
    }
    //=======================================================
    // Menu Scroll
    //=======================================================
    $('.mainNav ul li.scroll a').on('click', function() {
        $('html, body').animate({scrollTop: $(this.hash).offset().top - 68}, 1000);
        if($(window).width() < 767)
        {
            $('.mainNav > ul').slideUp('slow');
            $('.mobileMenu').removeClass('active');
        }
        return false;
    });

    $(window).on('scroll', function() {
        Scroll();
    });

    function Scroll() {

        var contentTop = [];
        var contentBottom = [];
        var winTop = $(window).scrollTop();
        var rangeTop = 200;
        var rangeBottom = 500;

        $('.mainNav').find('li.scroll > a').each(function() {
            var atr = $(this).attr('href');

            if ($(atr).length > 0)
            {
                contentTop.push($($(this).attr('href')).offset().top);
                contentBottom.push($($(this).attr('href')).offset().top + $($(this).attr('href')).height());
            }

        });

        $.each(contentTop, function(i) {

            if (winTop > contentTop[i] - rangeTop) {
                $(".mainNav li").removeClass('active');
                $('.mainNav li.scroll')
                        .removeClass('active')
                        .eq(i).addClass('active');
            }
        });

    }

    //=======================================================
    // magnificPopup
    //=======================================================
    if ($('a.popup').length > 0) {
        $("a.popup").magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            }
        });
    }

    //===================================
    // Fixed Header
    //===================================
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 40)
        {
            $("header").addClass('fixedHeader animated fadeInUp');
        }
        else
        {
            $("header").removeClass('fixedHeader animated fadeInUp');
        }
    });
    //========================
    // Contact Submit
    //========================
    if ($("#booking").length > 0)
    {
        $("#booking").on('submit', function(e) {
            e.preventDefault();
            $("#con_submit").html('Processsing...');

            var allData = $(this).serialize();

            var required = 0;
            $(".required", this).each(function() {
                if ($(this).val() == '')
                {
                    $(this).addClass('reqError');
                    required += 1;
                }
                else
                {
                    if ($(this).hasClass('reqError'))
                    {
                        $(this).removeClass('reqError');
                        if (required > 0)
                        {
                            required -= 1;
                        }
                    }
                }
            });
            if (required === 0)
            {
                if ($('#a').is(':checked'))
                {
                    $('.cheackbox').removeClass('agreeReq');
                    $.ajax({
                        type: "POST",
                        url: 'php/mail.php',
                        data: {allData: allData},
                        success: function(data)
                        {
                            $("#con_submit").html('<i>Done!</i><span></span>');
                            $("#booking input").val('');
                            $(".contactSuccess").fadeIn('slow');
                            setTimeout(function() {
                                $(".contactSuccess").fadeOut('slow');
                            }, 2500);
                        }
                    });
                }
                else
                {
                    $('.cheackbox').addClass('agreeReq');
                    $("#con_submit").html('<i>Failed!</i> <span></span>');
                }
            }
            else
            {
                $("#con_submit").html('<i>Failed!</i> <span></span>');
            }

        });

        $(".required").on('keyup', function() {
            $(this).removeClass('reqError');
        });
    }


    if ($("#subscriptionsforms").length > 0)
    {
        $("#subscriptionsforms").on('submit', function(e) {
            e.preventDefault();
            var sub_email = $("#sub_email").val();
            $("#sub_submit").html('Processing...');
            if (sub_email == '')
            {
                $("#sub_email").addClass('reqError');
                $("#sub_submit").html('Failed!');
            }
            else
            {
                $("#sub_email").removeClass('reqError');
                $.ajax({
                    type: "POST",
                    url: "php/subscription.php",
                    data: {sub_email: sub_email},
                    success: function(data)
                    {
                        $("#subscriptionsforms input").val('');
                        $("#sub_submit").html('Done!');
                        $(".subscriptionSuccess").fadeIn('slow');
                        setTimeout(function() {
                            $(".subscriptionSuccess").fadeOut('slow');
                        }, 2500);
                    }
                });
            }
        });
        $("#sub_email").on('keyup', function() {
            $(this).removeClass('reqError');
        });
    }
    $(document).mouseup(function(e) {
        var container = $(".closers");

        if (!container.is(e.target) && container.has(e.target).length === 0)
        {
            $(".subscriptionSuccess").fadeOut('slow');
        }
        if (!container.is(e.target) && container.has(e.target).length === 0)
        {
            $(".contactSuccess").fadeOut('slow');
        }
    });
    //========================
    // Wow Js
    //========================
    new WOW().init();

    //========================
    // Back To Top
    //========================
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > $(window).height())
        {
            $("#backToTop").addClass('showit');
        }
        else
        {
            $("#backToTop").removeClass('showit');
        }

    });
    $("body, html").on("click", "#backToTop", function(e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: 0}, 800);
    });
    //========================
    // Loader 
    //========================
    $(window).load(function() {
        if ($('.preloader').length > 0) {
            $('.preloader').delay(800).fadeOut('slow');
        }
    });
    //========================
    // Slide Show Bg
    //========================
    $(".banner").vegas({
        transitionDuration: 4000,
        slides: [
            {src: "images/banner.jpg"},
            {src: "images/banner2.jpg"},
            {src: "images/banner3.jpg"}
        ],
        transition: 'fade'
    });


})(jQuery);
