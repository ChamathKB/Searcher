import { useRef, useEffect } from 'react';

const MOUNTED_STATES = {
	NEURAL: 'neural',
	TEXT: 'text',
	HYBRID: 'hybrid',
  };

const useMountedRef = () => {
	const mounted = useRef(MOUNTED_STATES.NEURAL);

	useEffect(() => {
		mounted.current = MOUNTED_STATES.NEURAL;

		return () => {
			// Update state based on the specific logic
			mounted.current = MOUNTED_STATES.TEXT; // Example update to 'text' state on unmount
		};
	}, []);

	return mounted;
};

export default useMountedRef;
