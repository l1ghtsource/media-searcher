import React from 'react';
import cl from "./FiltersMobileComponent.module.css";
import FilterBtn from '../../UI/FilterBtn/FilterBtn';
// import FacesComponent from '../FacesComponent/FacesComponent';

function FiltersMobileComponent({ filters, selectedOptions, toggleOption, faces }) {
  return (
    <div className={cl.filtersMobileComponent}>
      {filters &&
        filters.map((filter, index) => (
          <div key={index} className={cl.filterMobile}>
            <div className={cl.filterMobile__title}>{filter.title}</div>
            <div className={cl.filterMobile__options}>
              {/* Отображаем выбранные опции первыми */}
              {selectedOptions[filter.title] &&
                Array.from(selectedOptions[filter.title]).map((option, i) => (
                  <FilterBtn
                    key={i}
                    onClick={() => toggleOption(filter.title, option.id)}
                    isActive={true}
                  >
                    {option.name}
                  </FilterBtn>
                ))}
              {/* Затем отображаем остальные опции */}
              {filter.options.map((option, i) => (
                !selectedOptions[filter.title]?.has(option.id) && (
                  <FilterBtn
                    key={i}
                    onClick={() => toggleOption(filter.title, option.id)}
                    isActive={selectedOptions[filter.title]?.has(option.id)}
                  >
                    {option.name}
                  </FilterBtn>
                )
              ))}
            </div>
          </div>
        ))}
        {/* <FacesComponent faces={faces} selectedOptions={selectedOptions} toggleOption={toggleOption}/> */}
    </div>
  );
}

export default FiltersMobileComponent;
