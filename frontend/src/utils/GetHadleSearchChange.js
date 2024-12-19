const GetHandleSearchChange = (debounceTimeout,
                               setLocalSearchValue,
                               ChangeValueInUpperComponent,
                               symbol_limit,
                               delay_ms) => (event) => {
    const searchValue = event.target.value;
    setLocalSearchValue(searchValue);

    // Очищаем предыдущий таймер
    if (debounceTimeout.current) {
        clearTimeout(debounceTimeout.current);
    }

    // Устанавливаем новый таймер
    debounceTimeout.current = setTimeout(() => {
        if (searchValue.length > symbol_limit || searchValue === "") {
            ChangeValueInUpperComponent(searchValue);
        }
    }, delay_ms); // Задержка
};

export default GetHandleSearchChange