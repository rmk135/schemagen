
//btn_add_field_schema
document.addEventListener('DOMContentLoaded', function() {

document.querySelector('#btn_add_field_schema').addEventListener('click', add_field);
document.querySelector('#btn_submit_schema').addEventListener('click', submit_schema);


var btns_gen_data = document.querySelectorAll('.btn_data_gen_');
for(i=0;i<btns_gen_data.length; i++){
         btns_gen_data[i].addEventListener('click', pre_generator_data);
         }
});

function pre_generator_data() {
    var schema_id = this.id
    var div = document.querySelector('#div_'+schema_id)
    var div_add = document.createElement('div');
        var count_input = document.createElement("INPUT");
        count_input.className = "form-group col-md-1"
        count_input.id =  "count_input_"+ schema_id

        var btn = document.createElement("BUTTON");
        btn.className = "btn btn-outline-primary";
        btn.innerText = '+';
        var name_input = document.createElement("INPUT");
        
        name_input.className = "form-group col-md-2"
        name_input.placeholder = "Name for table"
        name_input.id = "name_input"+schema_id

            div_add.innerHTML =  "";
            div_add.append(name_input)
            div_add.append("  count rows: ")
            div_add.append(count_input)
            div_add.append(" ")
            div_add.append(btn)

        btn.addEventListener('click', () => generation_data(schema_id));
    div.append(div_add)

}

function generation_data(schema_id) {
    count_rows = document.querySelector('#count_input_'+schema_id).value;
    table_name =document.querySelector('#name_input'+schema_id).value;

    fetch('/generation_data', {
          credentials: 'include',
          method: 'POST',
          body: JSON.stringify({
              "schema_id": schema_id,
              "count_rows": count_rows,
              "table_name": table_name
          })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result.data);
        });
}

function submit_schema() {
    var name = document.querySelector('#schema_name').value;
    console.log(name)

    fetch('/submit_schema', {
          credentials: 'include',
          method: 'POST',
          body: JSON.stringify({
              name: name
          })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result.data);
        });
}

function add_field() {
    var name = document.querySelector('#colum_name_new').value;
    var kind =  document.querySelector('#colum_type_new').value;
    var order =  document.querySelector('#colum_order_new').value;

    fetch('/add_custom_field', {
          credentials: 'include',
          method: 'POST',
          body: JSON.stringify({
              name: name,
              order:order,
              kind:kind
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            document.querySelector('#colum_name_new').value = '';
            document.querySelector('#colum_order_new').value = '';
            visualisation_add_column(result.data);
        });

}

function visualisation_add_column(column){
console.log(column)
    rows = document.querySelector('#custom_colums')
        var field = document.createElement('div');
        field.className = 'form-row';
            var div_for_name = document.createElement('div');
                div_for_name.className = 'form-group col-md-6';
                var label = '<label for="input_name_'+column.id +'"  class="text-black-50 mb-0">Column name</label>';
                var input = '<input type="text" class="form-control" id="input_name_'+column.id +'" value="'+ column.name+'">';
        div_for_name.innerHTML = label + input;
        field.append(div_for_name)
            var div_for_type = document.createElement('div');
                div_for_type.className = 'form-group col-md-2';
                label = '<label for="inputState_"  class="text-black-50 mb-0">Type</label>'
                var select = document.createElement('select');
                    select.className = 'form-control'
                    var option = ''
                    const select_ = document.querySelector('#colum_type_new').getElementsByTagName('option')
                    for (let i = 0; i < select_.length; i++) {
                        option = '<option>'+ select_[i].textContent+'</option>'
                        select.innerHTML += option

                        selected_i = 0;
                        if (select[i].textContent === column.kind)
                         {
                            select[i].selected = true;
                            console.log(" = = = = = = = = = = = = = = =  selected " )
                            console.log("select[i].textContent = " select[i].textContent)
                         }

                    }

            div_for_type.innerHTML = label;
            div_for_type.append(select)
        field.append(div_for_type)

        var div_for_order = document.createElement('div');
                div_for_order.className = 'form-group col-md-2';
                var label = '<label for="input_order_'+column.id +'"  class="text-black-50 mb-0">Order</label>';
                var input = '<input type="text" class="form-control" id="input_order_'+column.id +'" value="'+ column.order+'">';
        div_for_order.innerHTML = label + input;
        field.append(div_for_order)


        var div_for_del = document.createElement('div');
                div_for_del.className = 'form-group col-md-2';
                var label = '<label  class="text-sm-black-50 mb-0"> </label>';
                var btn_del = '<a class="btn btn-outline-primary js-scroll-trigger" id="btn_delete_schema_'+column.id+'" href="#">delete</a>';
        div_for_del.innerHTML = label + btn_del;
        field.append(div_for_del)



    rows.append(field)
}


