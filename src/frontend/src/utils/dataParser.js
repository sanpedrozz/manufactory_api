/**
 * Парсер для преобразования данных переменных в нужный формат.
 * @param {string} input - строка с данными переменных.
 * @returns {object} - объект с распарсенными переменными.
 */
export const parseData = (input) => {
    const lines = input.trim().split('\n');  // Разделяем входной текст по строкам
    let currentPrefix = '';  // Переменная для хранения текущего префикса (если есть)
    const result = {};

    // Массив базовых типов данных, которые не являются составными структурами
    const nonComplexTypes = ['Int', 'UDInt', 'USInt', 'DInt', 'String', 'Bool', 'Real', 'Byte'];

    lines.forEach((line) => {
        const [name, type, address] = line.split('\t');  // Разделяем строку на части

        if (!name || !type || !address) return;  // Если какая-то часть отсутствует, пропускаем строку

        // Проверяем, является ли тип строкой с указанием длины (например, "String[15]")
        const stringTypeMatch = type.match(/^String\[(\d+)\]$/);

        // Если тип переменной является составной структурой (например, Struct, DTL) или неизвестной строкой
        if (!nonComplexTypes.includes(type) && !stringTypeMatch) {
            currentPrefix = name;  // Устанавливаем текущий префикс для составной структуры
        } else {
            // Если строка имеет тип вида "String[15]"
            let variableType = type;
            if (stringTypeMatch) {
                variableType = `String[${stringTypeMatch[1]}]`;  // Оставляем информацию о длине строки
            }

            // Если есть префикс, добавляем его к названию переменной
            const variableName = currentPrefix ? `${currentPrefix}.${name}` : name;

            // Добавляем переменную в результат
            result[variableName] = {
                type: variableType,
                address
            };
        }
    });

    return result;
};
