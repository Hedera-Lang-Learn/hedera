import { TOGGLE_SIDEBAR_LEFT, TOGGLE_SIDEBAR_RIGHT } from '../constants';

export default {
  [TOGGLE_SIDEBAR_LEFT]: (state) => {
    state.sidebarLeftOpened = !state.sidebarLeftOpened;
  },
  [TOGGLE_SIDEBAR_RIGHT]: (state) => {
    state.sidebarRightOpened = !state.sidebarRightOpened;
  },
};
