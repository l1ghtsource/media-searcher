import React, { useState } from 'react'
import cl from "./FiltersComponent.module.css"
import FilterBtn from '../../UI/FilterBtn/FilterBtn'

function FiltersComponent({filters}) {
    const [visibleFilters, setVisibleFilters] = useState(1);
    const [expanded, setExpanded] = useState({ 0: true });
    const [selectedOptions, setSelectedOptions] = useState({});

    //Функция для показа всех фильтров
    const showAllFilters = () => {
        setVisibleFilters(filters.length);
        setExpanded(prevState => {
            const newState = { ...prevState };
            filters.forEach((_, index) => {
                if(index !== 0){
                    newState[index] = false; // Раскрываем все фильтры
                }
            });
            return newState;
        });
    }

    //Функция для раскрытия всех фильтров
    const hideAllFilters = () => {
        setVisibleFilters(1);
        setExpanded({ 0: true });
        console.log(selectedOptions);
    }

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
    <div>
        <div className={cl.filters}>
            {
                //* Показать все фильтры
                filters && filters.slice(0, visibleFilters).map((filter, index) => (
                    <div key={index}>
                        <div className={cl.filters__title} onClick={() => toggleOptions(index)}>{filter.title}</div>
                        <div className={cl.filters__options}>
                        {   
                            filter.options.slice(0, expanded[index] ? filter.options.length : 0).map((option, index) => (
                                <FilterBtn 
                                    key={index}
                                    onClick={() => toggleOption(filter.title, option)}
                                    isActive={selectedOptions[filter.title] && selectedOptions[filter.title].has(option)}
                                >{option}</FilterBtn>
                            ))
                        }
                        </div>
                        {/* {
                            index === 0 && visibleFilters !== filters.length && (
                                <div className={cl.filters__btn} onClick={() => toggleOptions(index)}>
                                    {expanded[index] ? 'Скрыть' : 'Больше'}
                                </div>
                            )
                        } */}
                                        
                    </div>
                ))
            }

            {/* //* Условия для показа кнопки фильтров */}
            {
            filters.length > 1 && (
            visibleFilters < filters.length 
            ?
                <div className={cl.filters__btn} onClick={showAllFilters}>
                Показать все фильтры
                </div>
            :
                <div className={cl.filters__btn} onClick={hideAllFilters}>
                Скрыть все фильтры
                </div>
            )
        }
        </div>
        {/* <div className={cl.filters__submit_btn}>
            Отправить выбранные фильтры
        </div> */}
    </div>
  )
}

export default FiltersComponent