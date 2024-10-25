function initializeTelegram() {
    let tg = window.Telegram.WebApp;

    // Проверка наличия данных
    if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        let userId = tg.initDataUnsafe.user.id;
        return userId;
    } else {
        return null;
    }
}

// Экспорт переменной userId
let userId = initializeTelegram();
export { userId };