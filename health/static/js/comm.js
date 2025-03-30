const menuItems = document.querySelectorAll('.menu-item');


// remove active clss from all the items
const changeActiveItem = () => {
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}


menuItems.forEach(item => {
    item.addEventListener('click', () => { 
           changeActiveItem();
        item.classList.add('active');
        if(item.id != 'notifications'){
            document.querySelector('.notifications-popup').
            style.display = 'none';
        } else {
            document.querySelector('notifications-popup').
            style.display = 'block';
        }
    })
})