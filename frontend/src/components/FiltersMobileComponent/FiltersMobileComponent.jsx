import React, { useState } from 'react';
import cl from "./FiltersMobileComponent.module.css";
import FilterBtn from '../../UI/FilterBtn/FilterBtn';
import FacesMobileComponent from '../FacesMobileComponent/FacesMobileComponent';
import fold from '../../assets/svgIcons/fold.svg';

function FiltersMobileComponent({ filters, selectedOptions, toggleOption, faces }) {
  const [expanded, setExpanded] = useState({});
  const expandedStart = 4;

  // Функция для раскрытия опций в фильтре
  const toggleOptions = (index) => {
      setExpanded(prevState => ({
          ...prevState,
          [index]: !prevState[index]
      }));
  };

  // Функция для получения отсортированных опций с учетом выбранных
  const getSortedOptions = (filter) => {
    const selected = selectedOptions[filter.title] || new Set();
    const unselectedOptions = filter.options.filter(option => !selected.has(option.id));
    return [
      ...filter.options.filter(option => selected.has(option.id)),
      ...unselectedOptions
    ];
  };

  return (
    <div className={cl.filtersMobileComponent}>
      {filters &&
        filters.map((filter, index) => (
          <div key={index} className={cl.filterMobile}>
            <div className={cl.filterMobile__title}>{filter.title}</div>
            <div className={cl.filterMobile__options}>
              {getSortedOptions(filter).slice(0, expanded[index] ? filter.options.length : expandedStart).map((option, i) => (
                <FilterBtn
                  key={i}
                  onClick={() => toggleOption(filter.title, option.id)}
                  isActive={selectedOptions[filter.title]?.has(option.id)}
                >
                  {option.name}
                </FilterBtn>
              ))}
            </div>
            {
              filter.options.length > expandedStart && (
                expanded[index]
                ?
                  <div className={cl.fold} onClick={() => toggleOptions(index)}>
                    <img src={fold} alt="fold" />
                  <div className={cl.fold__text}>Свернуть</div>
                  </div>
                :
                  <div className={cl.expand} onClick={() => toggleOptions(index)}>Больше</div>
              )
             }
          </div>
        ))}
      <FacesMobileComponent faces={faces} selectedOptions={selectedOptions} toggleOption={toggleOption} />
    </div>
  );
}

export default FiltersMobileComponent;
