import React, { useState } from 'react';
import axios from 'axios';

const AddDataPage = () => {
  const [places, setPlaces] = useState([]);
  const [selectedPlace, setSelectedPlace] = useState('');
  const [dataBlocks, setDataBlocks] = useState([{ block: '', data: '' }]);

  // Fetch places from API
  const fetchPlaces = async () => {
    const response = await axios.get('http://localhost:7000/api/places');
    setPlaces(response.data);
  };

  // Add another data block
  const addDataBlock = () => {
    setDataBlocks([...dataBlocks, { block: '', data: '' }]);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    const payload = dataBlocks.map((item) => ({
      data_block: item.block,
      data: item.data.split('\n').reduce((acc, line) => {
        const [name, type, address] = line.split('\t');
        acc[name] = { type, address };
        return acc;
      }, {})
    }));
    await axios.post(`http://localhost:7000/api/places/${selectedPlace}/data`, { data: payload });
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
          onFocus={fetchPlaces}
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
