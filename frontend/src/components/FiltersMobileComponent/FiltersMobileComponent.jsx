import React from 'react'
import cl from "./FiltersMobileComponent.module.css"
import FilterBtn from '../../UI/FilterBtn/FilterBtn';

function FiltersMobileComponent({filters, selectedOptions, toggleOption}) {
  return (
    <div className={cl.filtersMobile}>
        {
            filters && filters.map((filter, index) => (
                <div key={index} className={cl.filterMobile}>
                    <div className={cl.filterMobile__title}>{filter.title}</div>
                    <div className={cl.filterMobile__options}>
                        {
                            filter.options.map((option, i) => (
                                <FilterBtn
                                    key={i}
                                    onClick={() => toggleOption(filter.title, option)}
                                    isActive={selectedOptions[filter.title] && selectedOptions[filter.title].has(option)}
                                >
                                {option}
                                </FilterBtn>
                            ))
                        }
                    </div>
                </div>
            ))
        }
    </div>
  )
}

export default FiltersMobileComponent