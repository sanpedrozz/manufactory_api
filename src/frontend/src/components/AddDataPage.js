import React, {useState, useEffect} from 'react';
import axios from 'axios';

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
            data: item.data.split('\n').reduce((acc, line) => {
                const [name, type, address] = line.split('\t');
                if (name && type && address) { // Убедись, что все данные заполнены
                    acc[name] = {type, address};
                }
                return acc;
            }, {})
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
        <div>
            <h1>Add Data to Place</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="place">Select Place:</label>
                <select
                    id="place"
                    value={selectedPlace}
                    onChange={(e) => setSelectedPlace(e.target.value)}
                >
                    <option value="">-- Select Place --</option>
                    {places.map((place) => (
                        <option key={place.id} value={place.id}>{place.name}</option>
                    ))}
                </select>

                {dataBlocks.map((block, index) => (
                    <div key={index}>
                        <input
                            type="text"
                            placeholder="Data Block"
                            value={block.block}
                            onChange={(e) => {
                                const newDataBlocks = [...dataBlocks];
                                newDataBlocks[index].block = e.target.value;
                                setDataBlocks(newDataBlocks);
                            }}
                        />
                        <textarea
                            placeholder="Data"
                            value={block.data}
                            onChange={(e) => {
                                const newDataBlocks = [...dataBlocks];
                                newDataBlocks[index].data = e.target.value;
                                setDataBlocks(newDataBlocks);
                            }}
                        />
                    </div>
                ))}

                <button type="button" onClick={addDataBlock}>Add Data Block</button>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default AddDataPage;
