import React from 'react'
import cl from "./FiltersComponent.module.css"
import FilterBtn from '../../UI/FilterBtn/FilterBtn'

function FiltersComponent({filters}) {
  return (
    <div className={cl.filters}>
        {
            filters && filters.map((filter) => (
                <div>
                    <div className={cl.filters__title}>{filter.title}</div>
                    <div className={cl.filters__options}>
                    {   
                        filter && filter.options.map((option, index) => (
                            <FilterBtn key={index}>{option}</FilterBtn>
                        ))
                    }
                    </div>
                </div>
            ))
        }
    </div>
  )
}

export default FiltersComponent