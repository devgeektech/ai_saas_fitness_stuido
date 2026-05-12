$(document).ready(function () {

    function truncateText(text, length = 20) {

        if (!text) return "—";

        return text.length > length
            ? text.substring(0, length) + "..."
            : text;
    }

    let exercises_table = $('#studio-exercises-list').dataTable({

        serverSide: true,

        sAjaxSource: exercises_list,

        columns: [

            {
                name: "uuid",
                data: 0,
                visible: false
            },

            {
                name: "name",
                data: 1,
                render: function (data, type) {

                    if (type === "display") {
                        return truncateText(data, 20);
                    }

                    return data;
                }
            },

            {
                name: "category",
                data: 2,
                render: function (data, type) {

                    if (type === "display") {
                        return truncateText(data, 20);
                    }

                    return data;
                }
            },

            {
                name: "difficulty",
                data: 3,
                render: function (data, type) {

                    if (type === "display") {
                        return truncateText(data, 15);
                    }

                    return data;
                }
            },

            {
                name: "muscle_group",
                data: 4,
                render: function (data, type) {

                    if (type === "display") {
                        return truncateText(data, 20);
                    }

                    return data;
                }
            },

            {
                name: "status",
                data: 5,
                render: function (data, type) {

                    if (type === "display") {

                        if (data === "approved") {
                            return "✅ Approved";
                        }

                        if (data === "draft") {
                            return "📝 Draft";
                        }
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

                    return `
                    
                        <a href="/studio/exercises/view/${uuid}" class="action-icon">
                            <i class="mdi mdi-eye"></i>
                        </a>

                        <a href="/studio/exercises/edit/${uuid}" class="action-icon">
                            <i class="mdi mdi-square-edit-outline"></i>
                        </a>

                        <a href="javascript:void(0);"
                           class="action-icon confirmDeletion"
                           data-uuid="${uuid}">
                            <i class="mdi mdi-delete"></i>
                        </a>
                    `;
                }
            }
        ],

        order: [[6, 'desc']]
    });


    // OPEN DELETE MODAL
    $(document).on("click", ".confirmDeletion", function () {

        let uuid = $(this).attr("data-uuid");

        $(".deleteBtn").attr("data-uuid", uuid);

        $("#delete-alert-modal").modal('toggle');
    });


    // DELETE
    $(document).on("click", ".deleteBtn", function () {

        let uuid = $(this).attr("data-uuid");

        $.ajax({

            url: `/studio/exercises/delete/${uuid}`,

            type: "POST",

            data: {
                "csrfmiddlewaretoken":
                    $('input[name="csrfmiddlewaretoken"]').val()
            },

            success: function (data) {

                if (data.success) {

                    exercises_table.api().ajax.reload(null, false);

                    toastr.success(data.message);

                } else {

                    toastr.error(data.error);
                }
            }
        });
    });
});