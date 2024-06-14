import React, { forwardRef } from 'react';
import search from '../../assets/svgIcons/search.svg';
import cl from './SearchInput.module.css';

const SearchInput = forwardRef(({ value, onChange, onKeyDown, onFocus, onBlur }, ref) => {
  return (
    <div className={cl.search}>
      <img src={search} alt="search" className={cl.searchImg} />
      <input
        type="search"
        className={cl.searchInput}
        placeholder="Поиск"
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        onFocus={onFocus}
        onBlur={onBlur}
        ref={ref}
      />
    </div>
  );
});

export default SearchInput;
