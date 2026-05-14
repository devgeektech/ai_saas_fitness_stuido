$(document).ready(function () {
    function truncateText(text, length = 20) {
        if (!text) return "—";
        return text.length > length ? text.substring(0, length) + "..." : text;
    }

    function buildLegacyParams(data) {
        let params = {
            iDisplayStart: data.start,
            iDisplayLength: data.length,
            sEcho: data.draw,
            sSearch: data.search ? data.search.value : "",
            iSortingCols: data.order ? data.order.length : 0,
        };

        if (data.order) {
            data.order.forEach(function (orderItem, index) {
                params['iSortCol_' + index] = orderItem.column;
                params['sSortDir_' + index] = orderItem.dir;
            });
        }

        if (data.columns) {
            data.columns.forEach(function (column, index) {
                params['mDataProp_' + index] = column.data;
                params['sSearch_' + index] = column.search ? column.search.value : "";
            });
        }

        return params;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    let studios_table = $('#superadmin-studios-list').DataTable({
        serverSide: true,
        ajax: {
            url: studios_list,
            data: function (data) {
                return $.extend({}, data, buildLegacyParams(data));
            }
        },
        columns: [
            { name: "uuid", data: 0, visible: false },
            {
                name: "first_name",
                data: 1,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data || "-", 20);
                    }
                    return data;
                }
            },
            {
                name: "last_name",
                data: 2,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data || "-", 20);
                    }
                    return data;
                }
            },
            {
                name: "email",
                data: 3,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data, 30);
                    }
                    return data;
                }
            },
            {
                name: "username",
                data: 4,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data, 20);
                    }
                    return data;
                }
            },
            {
                name: "role",
                data: 5,
                render: function (data, type) {
                    if (type === "display") {
                        if (!data) return "-";
                        return data.charAt(0).toUpperCase() + data.slice(1);
                    }
                    return data;
                }
            },
            {
                name: "studio_name",
                data: 6,
                render: function (data, type) {
                    if (type === "display") {
                        return truncateText(data, 25);
                    }
                    return data;
                }
            },
            {
                name: "is_active",
                data: 7,
                render: function (data, type, row) {
                    if (type === "display") {
                        let checked = data === true || data === 'True' || data === 'true' ? "checked" : "";
                        return `<label class="form-check form-switch mb-0">
                                    <input type="checkbox" id="studio_status_${row[0]}" ${checked} class="form-check-input studio_user_status" data-user_uuid="${row[0]}">
                                    <span class="form-check-label">${checked ? "Active" : "Inactive"}</span>
                                </label>`;
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
                            <a href="/admin/studios/view/${uuid}" class="action-icon viewbtn">
                                <i class="mdi mdi-eye"></i>
                            </a>
                        `;
                    }
                    return data;
                }
            }
        ],
        order: [[1, 'asc']]
    });

    $(document).on('change', '.studio_user_status', function () {
        const checkbox = $(this);
        const uuid = checkbox.data('user_uuid');
        const url = studios_toggle_status_url.replace('00000000-0000-0000-0000-000000000000', uuid);
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').first().val() || csrftoken;

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            headers: {
                'X-CSRFToken': csrfToken,
            },
            success: function (response) {
                if (response.success) {
                    toastr.success('User status updated.');
                    studios_table.ajax.reload(null, false);
                } else {
                    toastr.error(response.message || 'Unable to update user status.');
                }
            },
            error: function () {
                toastr.error('Unable to update user status.');
            }
        });
    });

});
