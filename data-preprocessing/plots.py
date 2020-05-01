# make a color map of fixed colors
# first plot the image of how std changes across locations
cmap = mpl.colors.ListedColormap(['blue','green','red'])
bounds=[0,5,15,50]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
img = plt.imshow(image_std, #[0:50, 200:250], #interpolation='nearest',
                    cmap = cmap,norm=norm)

# make a color bar of the std sedimentation values
plt.colorbar(img,cmap=cmap,
                norm=norm,boundaries=bounds,ticks=[5,15,50])

plt.savefig('image_std.jpg')
plt.show()
plt.title('mean sediment over time')
