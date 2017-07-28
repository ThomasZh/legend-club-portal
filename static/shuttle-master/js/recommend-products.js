 // @2017/07/05
$(function(){

      var api_domain = $("#api_domain").val();
      var access_token = $("#access_token").val();
      var club_id = $("#club_id").val();
      var recommend_id = $("#recommend_category_id").val();
      // console.log(recommend_id);
      function getCartPro(pageNum) {
          var limit = 1000;//初始化值
          $.ajax({
            type: "GET",
            url: api_domain+"/api/item-recommend/categories/"+ recommend_id +"/items?page="+pageNum+"&limit="+limit,
            headers: {"Authorization": "Bearer "+ access_token +""},
            contentType: 'application/json',
            success: function(data, status, xhr) {
                  // console.log(data);
                  data_obj = JSON.parse(data);
                  data = data_obj.rs;
              var pageData = data.data;
              var inner_html = "";
              // console.log(pageData);
              for (var i in pageData) {
                  inner_html += '<li class="collection-item avatar list-item-info">';
                  inner_html += '<img src="'+pageData[i].img+'" alt="" class="circle" style="border-radius:0;">';
                  inner_html += '<span class="title">'+pageData[i].item_title+'</span>';
                  inner_html += '<p>品牌: '+pageData[i].brand_title+'</p>';
                  inner_html += '<p>规格: '+pageData[i].spec_title+'</p>';
                  inner_html += '<div class="hilight flex-separate">';
                  inner_html += '<input type="hidden" value="'+ pageData[i].spec_id +'" class="fee_template">';
                  inner_html += '<input type="hidden" value="'+ pageData[i].item_id +'" class="item_id">';
                  inner_html += '<span class="one-price">'+pageData[i].amount/100+'元/桶</span>';
                  inner_html += '<div class="qunatity">';
                  inner_html += '<a href="#!" class="counter del" data_dele_id="'+pageData[i]._id+'" data_pro_id="'+pageData[i].item_id+'"><i class="ion-minus-circled"></i></a>';
                  inner_html += '<span class="one-quantity">'+pageData[i].quantity+'</span>';
                  inner_html += '<a href="#!" class="counter add" data_dele_id="'+pageData[i]._id+'"><i class="ion-plus-circled"></i></a>';
                  inner_html += '</div></div>';
                  inner_html += '<a href="javascript:;" class="close cart-info-delete" data_dele_id="'+pageData[i]._id+'">';
                  inner_html += '<i class="iconfont icon-close ion-ios-close-empty"></i>';
                  inner_html += '</a>';
                  inner_html += '</li>';
                };
                $('#list-item').append(inner_html);
                // 减数量
                $(document).on("click",".del",function(){
                  var num = $(this).next().text();
                    if(num < 2){
                      num = 1;
                      $(this).next().text(num);
                    }else{
                      num--;
                      var _id = $(this).attr("data_dele_id");
                      // console.log(_id);
                      var data = {"quantity":num}
                      var  _json = JSON.stringify(data);
                      var _this = $(this);
                      $.ajax({
                        type: "POST",
                        url: api_domain+"/api/clubs/"+ club_id +"/cart/items/"+_id,
                        data:_json,
                        headers: {"Authorization": "Bearer "+ access_token +""},
                        contentType: 'application/json',
                        success: function(data, status, xhr) {
                          var data = JSON.parse(data);
                          var quantity = data.data.quantity;
                          _this.next().text(quantity);
                          getTotal();
                        }
                      });
                    }
                });
                // add product_num
                $(document).on("click",".add",function(){
                  var num = $(this).prev().text();
                      num++;
                  var _id = $(this).attr("data_dele_id");

                  var  data = {"quantity":num}
                  var  _json = JSON.stringify(data);
                    // console.log(_json);
                    var _this = $(this);
                    $.ajax({
                      type: "POST",
                      url: api_domain+"/api/clubs/"+ club_id +"/cart/items/"+_id,
                      data:_json,
                      headers: {
                        "Authorization": "Bearer "+ access_token +""
                      },
                      contentType: 'application/json',
                      success: function(data, status, xhr) {
                        // console.log(data);
                        var data = JSON.parse(data);
                        var quantity = data.data.quantity;
                        _this.prev().text(quantity);
                        getTotal();
                      }
                    });

                });
                // blur input save
                $(document).on("blur",".J_input",function(){
                    var _id = $(this).next().attr("data_dele_id");
                    var _this = $(this);
                    var num = $(this).val();
                    var data = {"quantity":num}
                    var _json = JSON.stringify(data);
                    $.ajax({
                      type: "POST",
                      url: api_domain+"/api/clubs/"+ club_id +"/cart/items/"+_id,
                      data:_json,
                      headers: {
                        "Authorization": "Bearer "+ access_token +""
                      },
                      contentType: 'application/json',
                      success: function(data, status, xhr) {
                        // console.log(data);
                        var data = JSON.parse(data);
                        var quantity = data.data.quantity;
                        _this.prev().val(quantity);
                        getTotal();
                      }
                    });
                });
                // watch input change
                $(document).on("input",".J_input",function(){
                    getTotal();
                });

                // 删除购物车一项
                $(document).on('click','.cart-info-delete',function(){
                  var _id = $(this).attr('data_dele_id');
                  var _this = $(this);
                  $.confirm("确定删除该商品吗?", function() {
                      $.ajax({
                        type: "DELETE",
                        url: api_domain+"/api/clubs/"+ club_id +"/cart/items/"+_id,
                        headers: {"Authorization": "Bearer "+ access_token +""},
                        contentType: 'application/json',
                        success: function(data, status, xhr) {
                          // location.reload();
                          _this.parent().remove();
                        }
                      });
                    }, function() {
                    //点击取消后的回调函数
                    });
                });
                // 导入购物车操作
                $("#put-cart-btn").on('click',function(event){
                      var specsArr = [];
                      var itemsArr = [];
                      var quantitysArr = [];
                      var data = [];
                  $('.fee_template').each(function(key,value){
                       specsArr[key] = $(this).val();
                  });
                  $('.item_id').each(function(key,value){
                       itemsArr[key] = $(this).val();
                  });
                  $('.one-quantity').each(function(key,value){
                       quantitysArr[key] = $(this).text();
                  });

                  for (var i=0; i<specsArr.length;i++){
                    var obj = {"item_id":itemsArr[i], "spec_id":specsArr[i], "quantity":quantitysArr[i]};
                    data.push(obj);
                  }
                  var json = JSON.stringify(data);
                  console.log(json);
                  $.ajax({
                    type: "POST",
                    url: api_domain+"/api/clubs/"+ club_id +"/cart/items",
                    data: json,
                    dataType: "json",
                    headers: {"Authorization":"Bearer "+access_token+""},
                    contentType: 'application/json',
                    success: function(data, status, xhr) {
                      location.href="/bf/wx/vendors/"+ club_id +"/items/cart"
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        console.log("error");
                    },
                    complete: function(XMLHttpRequest, textStatus) {
                      this; // 调用本次AJAX请求时传递的options参数
                    }
                  });
                });
              }
            })
      };
      getCartPro('1');

});
