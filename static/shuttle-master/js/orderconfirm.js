// @2017/07/05
$(function(){
    getTotal();
      // 计算总金额
      function getTotal(){
        var num = $(".list-item-info").length;
        var total_price=0;
        for(var i=0;i<num;i++){
          var one_price = $(".list-item-info").eq(i).find(".one-price").text();
          // console.log(one_price);
          var quantity = $(".list-item-info").eq(i).find(".one-quantity").text();
          // console.log(quantity);
          var one_total = parseFloat(one_price)*quantity;
              total_price += parseFloat(one_total);
        }
          $("#footer-bar span").text(total_price.toFixed(2));
      };

});
