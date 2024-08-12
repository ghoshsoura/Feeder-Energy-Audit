import styled from 'styled-components';

export const SelectContainer = styled.div`
    position: relative;
    width: 100%;
    max-width: 400px;
    margin: 20px 0;
`;

export const SelectInput = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #fff;
    cursor: pointer;

    &:hover {
        border-color: #888;
    }
`;

export const Dropdown = styled.ul`
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    z-index: 10;
    max-height: 200px;
    overflow-y: auto;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-top: 5px;
    padding: 0;
    list-style: none;
`;

export const DropdownItem = styled.li`
    padding: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;

    &:hover {
        background-color: #f0f0f0;
    }

    &.selected {
        background-color: #e6f7ff;
        font-weight: bold;
    }
`;

export const ClearButton = styled.button`
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin-left: 10px;
    color: #888;

    &:hover {
        color: #555;
    }
`;

export const SelectedItem = styled.span`
    display: inline-block;
    background-color: #f0f0f0;
    border-radius: 3px;
    padding: 5px 10px;
    margin: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
`;

export const SelectedItemsContainer = styled.div`
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
`;
