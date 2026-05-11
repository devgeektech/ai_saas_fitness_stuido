$(document).ready(function () {

    
    let check_status = $('.all-activity-level').val();
    $('.all-activity-level').on('change', function() {
        check_status = $(this).val();
        users_list_table.api().ajax.reload();
    });
    
    // let subscription_type = $('.all-subscription-type').val();
    // $('.all-subscription-type').on('change', function() {
    //     subscription_type = $(this).val();
    //     users_list_table.api().ajax.reload();
    // });

    // let role_filter = $('.role-filter').val();
    // $('.role-filter').on('change', function() {
    //     role_filter = $(this).val();
    //     users_list_table.api().ajax.reload();
    // });
    
    let users_list_table = $(document).find('#admin-users-agents-list').dataTable({
        serverSide: true,
        sAjaxSource: admin_users_list,
        fnServerParams: function (aoData) {
            aoData.push({ "name": "status", "value": check_status });
        },
        columns: [
            {name:"uuid", data:0, visible:false},
            {name: "full_name", data: 1},
            {name: "email", data: 2},
            {name: "role", data: 3},
            {
                name:"is_blocked",
                data: 4,
                render: function (data, type, row) {
                    if (type === 'display') {
                        let checked = row[4] === true ? "checked" : "";
                        return `<input type="checkbox" id="status_${row[0]}"  ${checked}  data-switch="bool" class="user_status" data-user_uuid="${row[0]}">
                        <label for="status_${row[0]}" data-on-label="Block" data-off-label="Unblock"></label>`;
                    }
                    return data;
                }
            },
            {
                name: "created_at",
                data: 5,
                render: function (data, type, row) {
                    if (type === 'display') {
                        if (data) {
                            let date = new Date(data);
                            let options = {
                                timeZone: 'America/New_York',
                                year: 'numeric',
                                month: '2-digit',
                                day: '2-digit',
                                hour: '2-digit',
                                minute: '2-digit',
                                second: '2-digit',
                                hour12: false
                            };
                            return date.toLocaleString('en-US', options);
                        } else {
                            return "—";
                        }
                    }
                    return data;
                }
            },
            {
                name:"action",
                data: null,
                render: function (data, type, row) {
                    if (type === 'display') {
                        return `<a href="users/${row[0]}" class="action-icon viewbtn"> <i class="mdi mdi-eye"></i></a>`;
                    }
                    return data;
                }
            }
        ],
        order: [[5, 'asc']],
    });
      
    //<a href="javascript:void(0);" class="action-icon confirmDeletion" data-uuid="${row[0]}"> <i class="mdi mdi-delete" data-bs-toggle="modal"></i></a> 
    // <a href="users/edit/${row[0]}" class="action-icon editBtn"> <i class="mdi mdi-square-edit-outline"></i></a>
    // Change User Status
    $(document).on("change",".user_status",function(){
        let status = false;
        if($(this).is(':checked')){status = true;}
        let user_uuid = $(this).data("user_uuid");
        $.ajax({
            url: `/admin/users/status/${user_uuid}`,  
            type: 'POST',
            data:{"csrfmiddlewaretoken":$('input[name="csrfmiddlewaretoken"]').val(),status,user_uuid},
            success: function(data) {
                // console.log({data});
                if(data.success){
                    toastr.success(data.message); 
                }else{
                    toastr.error(data.error);
                }
            }  
        });
    });

    // Open Confirm Delete Modal
    $(document).on("click",".confirmDeletion",function(){
        let uuid = $(this).attr("data-uuid");
        if(uuid){
            $(".deleteBtn").attr("data-uuid",uuid);
            $("#delete-alert-modal").modal('toggle');
        }
    });

    // Delete Type After Confirmation
    $(document).on("click",".deleteBtn",function(){
        let uuid = $(this).attr("data-uuid");
        $.ajax({
            url: `/admin/users/delete/${uuid}`,  
            type: 'POST',
            data:{"csrfmiddlewaretoken":$('input[name="csrfmiddlewaretoken"]').val()},
            success: function(data) {
                if(data.success){
                    users_list_table.api().ajax.reload();
                    toastr.success(data.message);
                }else{
                    toastr.error(data.error);
                }
            }  
        });
    });

});