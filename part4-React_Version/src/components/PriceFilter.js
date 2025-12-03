import React from 'react';

function PriceFilter({ value, onChange }) {
    return (
        <div className="filter-section">
            <label htmlFor="price-filter">Max Price:</label>
            <select id="price-filter" value={value} onChange={(e) => onChange(e.target.value)}>
                <option value="all">All</option>
                <option value="10">$10</option>
                <option value="50">$50</option>
                <option value="100">$100</option>
            </select>
        </div>
    );
}

export default PriceFilter;