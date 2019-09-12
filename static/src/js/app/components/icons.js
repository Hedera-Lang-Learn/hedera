import { faArrowRight } from '@fortawesome/free-solid-svg-icons/faArrowRight';
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons/faArrowLeft';
import { faCircle } from '@fortawesome/free-solid-svg-icons/faCircle';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons/faCaretDown';

const iconMap = [
  faArrowRight,
  faArrowLeft,
  faCircle,
  faCaretDown,
].reduce((map, obj) => {
  map[obj.iconName] = obj;
  return map;
}, {});

export default iconMap;
