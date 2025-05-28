document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const headerNav = document.querySelector('.header-nav');
    const menuItems = document.querySelectorAll('.menu-item > span');
    const headerRight = document.querySelector('.header-right');
    
    // Toggle menú hamburguesa
    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        headerNav.classList.toggle('active');
        document.body.classList.toggle('menu-open');
    });
    
    // Toggle submenús en móvil
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                const submenu = this.nextElementSibling;
                if (submenu) {
                    submenu.classList.toggle('active');
                }
            }
        });
    });
    
    // Cerrar menú al hacer clic en un enlace
    document.querySelectorAll('.header-nav a').forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                hamburger.classList.remove('active');
                headerNav.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
    });
    
    // Cerrar menú al hacer clic fuera
    headerNav.addEventListener('click', function(e) {
        if (e.target === this) {
            hamburger.classList.remove('active');
            this.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });
    
    // Manejar redimensionamiento
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            hamburger.classList.remove('active');
            headerNav.classList.remove('active');
            document.body.classList.remove('menu-open');
            
            // Cerrar todos los submenús en desktop
            document.querySelectorAll('.sub-menu').forEach(submenu => {
                submenu.classList.remove('active');
            });
        }
        
        // Mostrar/ocultar header-right según tamaño
        if (window.innerWidth <= 768) {
            headerRight.style.display = 'none';
        } else {
            headerRight.style.display = 'block';
        }
    });
    
    // Inicializar estado del header-right
    if (window.innerWidth <= 768) {
        headerRight.style.display = 'none';
    }
});





function toggleMenu(button) {
    // Cerrar otros menús abiertos
    document.querySelectorAll('.menu-dropdown.show').forEach(openMenu => {
        if (openMenu !== button.nextElementSibling) {
            openMenu.classList.remove('show');
            // También quitamos la clase active de otros botones
            openMenu.previousElementSibling.classList.remove('menu-active');
        }
    });
    
    // Alternar el menú actual
    const menu = button.nextElementSibling;
    menu.classList.toggle('show');
    button.classList.toggle('menu-active');
    
    // Si el menú se está mostrando, agregamos un event listener para cerrarlo al hacer clic fuera
    if (menu.classList.contains('show')) {
        setTimeout(() => {
            document.addEventListener('click', closeMenuOnClickOutside);
        }, 10);
    } else {
        document.removeEventListener('click', closeMenuOnClickOutside);
    }
}

function closeMenuOnClickOutside(event) {
    if (!event.target.closest('.menu-opciones')) {
        document.querySelectorAll('.menu-dropdown.show').forEach(menu => {
            menu.classList.remove('show');
            menu.previousElementSibling.classList.remove('menu-active');
        });
        document.removeEventListener('click', closeMenuOnClickOutside);
    }
}