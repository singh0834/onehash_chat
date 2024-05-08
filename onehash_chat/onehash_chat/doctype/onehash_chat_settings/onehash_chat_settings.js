// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('OneHash Chat Settings', {

	onload: function(frm){
		// if (!frm.doc.__onload?.can_show_promo) return;

    const alert = $(`
        <div
            class="alert alert-primary alert-dismissable fade show d-flex justify-content-between border-0"
            role="alert"
        >
            <div>
                Don't have OneHash Chat account ?
                <a href="https://chat.onehash.ai/app/auth/signup" target="_blank" class="alert-link">
                    Click Here !
                </a>
            </div>
            <button
                type="button"
                class="close"
                data-dismiss="alert"
                aria-label="Close"
                style="outline: 0px solid black !important"
            >
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `).prependTo(frm.layout.wrapper);

    alert.on("closed.bs.alert", () => {
        frappe.db.set_global("ic_api_promo_dismissed", 1);
    });
	},
    after_save: function (frm) {
        localStorage.clear();
        window.location.reload(true);
	},
	fetch_contacts_now: function(frm){
		frappe.call({
			method: 'onehash_chat.api.fetch_contacts_from_chat',
			args: {},
			callback: function (r) {}
		});
		frappe.msgprint('Contacts Updated !');
	},
	get_user_profile: function(frm){
		frappe.call({
			method: 'onehash_chat.api.fetch_user_account',
			args: {},
			callback: function (r) {}
		});
	},
	post_contacts_to_chat: function(frm){
		frappe.call({
			method: 'onehash_chat.api.post_contacts_to_chat',
			args: {},
			callback: function (r) {}
		});
		
	}
});

