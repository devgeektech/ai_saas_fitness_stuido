$(document).ready(function () {

    function truncateText(text, length = 20) {

        if (!text) return "—";

        return text.length > length
            ? text.substring(0, length) + "..."
            : text;
    }

    let audio_table = $('#studio-audio-segments-list').dataTable({

        serverSide: true,

        sAjaxSource: audio_segments_list,

        columns: [

            {
                name: "uuid",
                data: 0,
                visible: false
            },

            {
                name: "segment",
                data: 1,
                render: function (data, type) {

                    if (type === "display") {
                        return truncateText(data, 20);
                    }

                    return data;
                }
            },

            {
                name: "voice_id",
                data: 2
            },

            {
                name: "duration",
                data: 3,
                render: function (data, type) {

                    if (type === "display") {

                        if (data) {
                            return data + " sec";
                        }

                        return "—";
                    }

                    return data;
                }
            },

            {
                name: "status",
                data: 4
            },

            {
                name: "created_at",
                data: 5,
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
                    
                        <a href="/studio/audio-segments/view/${uuid}" class="action-icon">
                            <i class="mdi mdi-eye"></i>
                        </a>

                        <a href="/studio/audio-segments/edit/${uuid}" class="action-icon">
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

        order: [[5, 'desc']]
    });


    $(document).on("click", ".confirmDeletion", function () {

        let uuid = $(this).attr("data-uuid");

        $(".deleteBtn").attr("data-uuid", uuid);

        $("#delete-alert-modal").modal('toggle');
    });


    $(document).on("click", ".deleteBtn", function () {

        let uuid = $(this).attr("data-uuid");

        $.ajax({

            url: `/studio/audio-segments/delete/${uuid}`,

            type: "POST",

            data: {
                "csrfmiddlewaretoken":
                    $('input[name="csrfmiddlewaretoken"]').val()
            },

            success: function (data) {

                if (data.success) {

                    audio_table.api().ajax.reload(null, false);

                    toastr.success(data.message);

                } else {

                    toastr.error(data.error);
                }
            }
        });
    });

});