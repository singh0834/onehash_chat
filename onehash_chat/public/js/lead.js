// var html;

// frappe.ui.form.on('Lead', {
    
//     refresh: async function (frm) {

//             frm.add_custom_button("Fetch Lead / Contact", async function () {
//                 fetchcl(frm)
//            }, __('<img src="https://aisensy.wpenginepowered.com/wp-content/uploads/2021/02/Untitled.png" height="35px" width="60px">'));
            
//     }
// });

// async function fetchcl(frm){
//     await frappe.call({
//         method: 'onehash_chat.api.fetch_contacts',
//         args: {},
//         callback: function (r) {}
//     });
// }