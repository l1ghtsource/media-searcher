import React, { forwardRef } from 'react';
import search from '../../assets/svgIcons/search.svg';
import cl from './SearchInput.module.css';

const SearchInput = forwardRef(({ value, onChange, onKeyDown, onFocus, onBlur }, ref) => {

  // Функция для установки фокуса на инпут
  const focusInput = () => {
    if (ref && ref.current) {
      ref.current.focus();
    }
  };

  return (
    <div className={cl.search}>
      <img src={search} alt="search" className={cl.searchImg} onClick={focusInput}/>
      <input
        type="search"
        className={cl.searchInput}
        placeholder="Поиск"
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        onFocus={onFocus}
        onBlur={() => setTimeout(onBlur, 100)}
        ref={ref}
      />
    </div>
  );
});

export default SearchInput;
