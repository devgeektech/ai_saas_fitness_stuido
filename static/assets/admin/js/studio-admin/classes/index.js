$(document).ready(function () {

    function truncateText(text, length = 10) {
        if (!text) return "—";
        return text.length > length ? text.substring(0, length) + "..." : text;
    }

    let classes_table = $('#studio-classes-list').DataTable({
        serverSide: true,
        sAjaxSource: admin_classes_list,

        columns: [
            
            { name: "uuid", data: 0, visible: false },
            {
                name: "title",
                data: 1,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data, 10);
                    }
                    return data;
                }
            },
            {
                name: "category",
                data: 2,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data, 10);
                    }
                    return data;
                }
            },
            {
                name: "difficulty",
                data: 3,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data, 10);
                    }
                    return data;
                }
            },
            {
                name: "duration",
                data: 4,
                render: function (data, type) {
                    if (type === "display") {
                        return data ? data + " min" : "—";
                    }
                    return data;
                }
            },
            {
                name: "status",
                data: 5,
                render: function (data, type) {
                    if (type === "display") {
                        if (data === "ready") return "✅ Ready";
                        if (data === "draft") return "📝 Draft";
                        if (data === "generating") return "⏳ Generating";
                        if (data === "failed") return "❌ Failed";
                        return data || "—";
                    }
                    return data;
                }
            },
            {
                name: "created_at",
                data: 6,
                render: function (data, type) {
                    if (type === "display") {
                        if (data) {
                            let date = new Date(data);
                            return date.toLocaleString();
                        }
                        return "—";
                    }
                    return data;
                }
            },
            {
                name: "action",
                data: null,
                orderable: false,
                searchable: false,
                render: function (data, type, row) {

                    let uuid = row[0];

                    if (type === "display") {
                        return `
                            <a href="/studio/classes/view   /${uuid}" class="action-icon viewbtn">
                                <i class="mdi mdi-eye"></i>
                            </a>

                            <a href="/studio/classes/edit/${uuid}" class="action-icon editBtn">
                                <i class="mdi mdi-square-edit-outline"></i>
                            </a>

                            <a href="javascript:void(0);" class="action-icon confirmDeletion" data-uuid="${uuid}">
                                <i class="mdi mdi-delete"></i>
                            </a>
                        `;
                    }

                    return data;
                }
            }
        ],

        order: [[6, 'desc']]
    });



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
            url: `/studio/classes/delete/${uuid}`,  
            type: 'POST',
            data:{"csrfmiddlewaretoken":$('input[name="csrfmiddlewaretoken"]').val()},
            success: function(data) {
                if(data.success){
                    classes_table.ajax.reload(null, false);
                    toastr.success(data.message);
                }else{
                    toastr.error(data.error);
                }
            }  
        });
    });

});