import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

def minor_tick(x, pos):
  if not x % 1.0:
    return ""
  return f"{x+0.5:.0f}"

def update(i, im, states):
  im.set_data(states[i])
  return im,

def animate(grid_size, states, file_name = "lions", cell_colors = ['#FFFFFF', '#808080', '#D2B48C']):
  # figure settings
  fig, ax = plt.subplots(figsize=(10,10))

  for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2)

  bounds = [0, 1, 2, 3]
  cmap = colors.ListedColormap(cell_colors)
  norm = colors.BoundaryNorm(bounds, cmap.N)

  loc_major = ticker.MultipleLocator(base=1.0)
  loc_minor = ticker.MultipleLocator(base=0.5)
  for_major = ticker.NullFormatter()
  for_minor = ticker.FuncFormatter(minor_tick)
  ax.xaxis.set_major_locator(loc_major)
  ax.yaxis.set_major_locator(loc_major)
  ax.xaxis.set_major_formatter(for_major)
  ax.yaxis.set_major_formatter(for_major)
  ax.xaxis.set_minor_locator(loc_minor)
  ax.yaxis.set_minor_locator(loc_minor)
  ax.xaxis.set_minor_formatter(for_minor)
  ax.yaxis.set_minor_formatter(for_minor)

  ax.grid(which='major', axis='both', color='k', linestyle='-', linewidth=2)
  ax.tick_params(which='both', left=False, bottom=False)

  # initial image
  im = plt.imshow(states[0], cmap=cmap, norm=norm, interpolation='nearest', extent=(0, grid_size, 0, grid_size))

  # colorbar (scaled to grid)
  aspect = 20
  pad_fraction = 0.5
  divider = make_axes_locatable(ax)
  width = axes_size.AxesY(ax, aspect=1./aspect)
  pad = axes_size.Fraction(pad_fraction, width+0.5)
  cax = divider.append_axes("top", size=width, pad=pad)

  cbar = plt.colorbar(im, cax=cax, ticks=[0.5,1.5,2.5], orientation='horizontal')
  cbar.ax.tick_params(size=0)
  cbar.ax.xaxis.set_ticks_position('top')
  cbar.ax.xaxis.set_label_position('top')
  cbar.ax.set_xticklabels(['Cleared', 'Contaminated', 'Lion'])

  # generate and save animation
  ani = animation.FuncAnimation(fig, func=update, fargs=(im,states), interval=1000, save_count=len(states), blit=True)
  ani.save(file_name + '.mp4')
