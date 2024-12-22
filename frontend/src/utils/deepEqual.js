function deepEqual(obj1, obj2) {
    // Проверяем, являются ли оба аргумента объектами
    if (obj1 === null || typeof obj1 !== 'object' || obj2 === null || typeof obj2 !== 'object') {
        return obj1 === obj2;
    }

    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);

    if (keys1.length !== keys2.length) {
        return false;
    }

    // Рекурсивно сравниваем каждый ключ
    for (let key of keys1) {
        if (!keys2.includes(key) || !deepEqual(obj1[key], obj2[key])) {
            return false;
        }
    }

    // Если все проверки пройдены, объекты равны
    return true;
}

export default deepEqual;