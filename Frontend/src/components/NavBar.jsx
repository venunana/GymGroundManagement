import React from "react";
import { useLocation, NavLink } from "react-router-dom";
import PropTypes from "prop-types";
import { Menu, X } from "lucide-react";

const NavBar = ({ onHamburgerClick, isLeftbarVisible }) => {
  const location = useLocation();

  const getNavPath = (pathname) => {
    const parts = pathname.split("/").filter(Boolean);

    if (parts.length === 0) {
      return (
        <NavLink to="/" className="text-black hover:underline">
          Home
        </NavLink>
      );
    }

    return parts.map((part, index) => (
      <React.Fragment key={part}>
        {index > 0 && (
          <span className="text-black mx-1">&gt;</span> // Arrow separator
        )}
        <NavLink
          to={`/${parts.slice(0, index + 1).join("/")}`}
          className={({ isActive }) =>
            `text-inf hover:underline ${isActive ? "font-bold" : ""}`
          } // Highlight the active link
        >
          {part.charAt(0).toUpperCase() + part.slice(1)}
        </NavLink>
      </React.Fragment>
    ));
  };

  return (
    <nav className="bg-white p-4 sticky top-0">
      <div className="flex items-center">
        {/* Hamburger Menu Icon */}
        <button className="block md:hidden mr-4" onClick={onHamburgerClick}>
          {isLeftbarVisible ? (
            <X className="w-6 h-6" /> // "X" icon
          ) : (
            <Menu className="w-6 h-6" /> // Hamburger icon
          )}
        </button>
        {/* Optional logo or brand name here */}
        <div className="ml-auto">{getNavPath(location.pathname)}</div>
      </div>
    </nav>
  );
};

NavBar.propTypes = {
  onHamburgerClick: PropTypes.func.isRequired,
  isLeftbarVisible: PropTypes.bool.isRequired,
};

export default NavBar;
