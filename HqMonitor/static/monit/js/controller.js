var values = [];
function get_r1_data() {
	$.ajax({
		url:"http://127.0.0.1:8000/test",
		type : 'get',
		dataType : 'json',
		success: function(data) {

			console.log(data.a)
			values[0]=data.a
			values[1]=data.b
			values[2]=data.c
			values[3]=data.d
			values[4]=data.e
			values[5]=data.f

			//数据遍历
			// $.each(data, function(index,values){   // 解析出data对应的Object数组
             //        $.each(values,function(index2,value){   // 遍历Object数组 ，每个对象的值存放在value ，index2表示为第几个对象
             //            //  根据自己的逻辑进行数据的处理
             //            alert(value.name + "  " + value.value);
             //           //  TODO:  逻辑
             //        });
             //    });
			$(Object.keys(data)).each(function(idx,e){
				console.log("key: " + e + " value: " + json[e]);
			});

			//alert(values)
			//调用js.js中的函数
			echarts_1(values);
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}
// get_r1_data()