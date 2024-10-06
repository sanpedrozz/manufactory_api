import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { parseData } from '../utils/dataParser';  // Импортируем парсер
import './AddDataPage.css'; // Подключаем стили

const AddDataPage = () => {
    const [places, setPlaces] = useState([]);
    const [selectedPlace, setSelectedPlace] = useState('');
    const [dataBlocks, setDataBlocks] = useState([{block: '', data: ''}]);

    // Fetch places from API on component mount
    useEffect(() => {
        const fetchPlaces = async () => {
            try {
                const response = await axios.get('http://localhost:7000/place/places');
                setPlaces(response.data);
            } catch (error) {
                console.error("Error fetching places:", error);
            }
        };
        fetchPlaces();
    }, []);

    // Add another data block
    const addDataBlock = () => {
        setDataBlocks([...dataBlocks, {block: '', data: ''}]);
    };

    // Handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault();

        const payload = dataBlocks.map((item) => ({
            data_block: Number(item.block), // Преобразуем в число
            data: parseData(item.data)      // Используем парсер для преобразования данных
        }));
        console.log("Данные для отправки:", payload);

        try {
            const response = await axios.post(`http://localhost:7000/place/places/${selectedPlace}/update_data_for_read`, payload);
            console.log("Ответ сервера:", response.data);
            alert('Data submitted successfully!');
        } catch (error) {
            console.error("Ошибка при отправке данных:", error.response ? error.response.data : error.message);
        }
    };

    return (
        <div className="container">
            <h1 className="title">Add Data to Place</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="place">Select Place:</label>
                    <select
                        id="place"
                        value={selectedPlace}
                        onChange={(e) => setSelectedPlace(e.target.value)}
                        className="form-select"
                    >
                        <option value="">-- Select Place --</option>
                        {places.map((place) => (
                            <option key={place.id} value={place.id}>{place.name}</option>
                        ))}
                    </select>
                </div>

                {dataBlocks.map((block, index) => (
                    <div key={index} className="data-block">
                        <input
                            type="text"
                            placeholder="Data Block"
                            value={block.block}
                            onChange={(e) => {
                                const newDataBlocks = [...dataBlocks];
                                newDataBlocks[index].block = e.target.value;
                                setDataBlocks(newDataBlocks);
                            }}
                            className="input-block"
                        />
                        <textarea
                            placeholder="Data"
                            value={block.data}
                            onChange={(e) => {
                                const newDataBlocks = [...dataBlocks];
                                newDataBlocks[index].data = e.target.value;
                                setDataBlocks(newDataBlocks);
                            }}
                            className="textarea-block"
                        />
                    </div>
                ))}

                <div className="buttons">
                    <button type="button" className="btn" onClick={addDataBlock}>Add Data Block</button>
                    <button type="submit" className="btn-submit">Submit</button>
                </div>
            </form>
        </div>
    );
};

export default AddDataPage;
