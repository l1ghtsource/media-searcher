import React, { useState } from 'react'
import cl from "./FiltersComponent.module.css"
import FilterBtn from '../../UI/FilterBtn/FilterBtn'
import fold from '../../assets/svgIcons/fold.svg'

function FiltersComponent({filters}) {
    const [expanded, setExpanded] = useState({});
    const [selectedOptions, setSelectedOptions] = useState({});
    const expandedStart = 4;

    //Функция для раскрытия опций в фильтре
    const toggleOptions = (index) => {
        setExpanded(prevState => ({
          ...prevState,
          [index]: !prevState[index]
        }));
    }

    //Функция для выбора опций
    const toggleOption = (filterTitle, option) => {
        setSelectedOptions(prevState => {
            const newState = { ...prevState };
            if (!newState[filterTitle]) {
                newState[filterTitle] = new Set();
            }
            if (newState[filterTitle].has(option)) {
                newState[filterTitle].delete(option);
            } else {
                newState[filterTitle].add(option);
            }
            return newState;
        });
    };

    return (
        <div className={cl.filters}>
            {
                //* Показать все фильтры
                filters && filters.map((filter, index) => (
                    <div key={index} className={cl.filter}>
                        <div className={cl.filter__title}>{filter.title}</div>
                        <div className={cl.filter__options}>
                        {   
                            filter.options.slice(0, expanded[index] ? filter.options.length : expandedStart).map((option, i) => (
                                <FilterBtn 
                                    key={i}
                                    onClick={() => toggleOption(filter.title, option)}
                                    isActive={selectedOptions[filter.title] && selectedOptions[filter.title].has(option)}
                                >{option}</FilterBtn>
                            ))
                        }
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
                ))
            }
        </div>
    )
}

export default FiltersComponent;
